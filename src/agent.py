import numpy as np
from sklearn.linear_model import LinearRegression

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from dotenv import load_dotenv
import os

from database import log_energy, get_energy_history

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)


class EnergyMonitoringAgent:

    def analyze_energy(self, user_id, energy_kwh):

        # Save data
        log_energy(user_id, energy_kwh)

        # Get history
        history = get_energy_history(user_id)
        values = [h[0] for h in history]

        prediction = None

        # ML MODEL (only runs with 2+ records)
        if len(values) >= 2:

            X = np.array(range(len(values))).reshape(-1, 1)
            y = np.array(values)

            model = LinearRegression()
            model.fit(X, y)

            prediction = float(model.predict([[len(values)]])[0])

        prompt = f"""
You are an AI energy assistant.

History: {values}
Current usage: {energy_kwh}
Prediction: {prediction}

Provide:
- efficiency analysis
- anomaly detection
- optimization tips
"""

        response = llm.invoke([HumanMessage(content=prompt)])

        return {
            "ml_prediction": prediction,
            "llm_analysis": response.content
        }