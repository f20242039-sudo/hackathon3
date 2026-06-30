# Chalo Miya! 🕌✨

**Chalo Miya!** is an AI-powered Hyderabad travel companion that helps users discover places, build personalized itineraries, and explore the city's rich culture with intelligent recommendations.

## Features

* 🗺️ Personalized trip planning
* 🤖 AI-powered itinerary generation
* 📍 Hyderabad attractions and recommendations
* 📝 Extract travel preferences from natural language
* 🎯 Smart recommendations based on user interests
* 💻 Interactive frontend interface
* ⚡ FastAPI backend with REST APIs

## Project Structure

```
hackathon3/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── database/
│   │   ├── extractor/
│   │   ├── models/
│   │   ├── recommender/
│   │   └── main.py
│   ├── requirements.txt
│   └── LICENSE
│
├── frontend/
│   ├── assets/
│   ├── components/
│   ├── services/
│   ├── utils/
│   ├── app.py
│   └── requirements.txt
│
└── README.md
```

## Tech Stack

### Backend

* Python 3.11+
* FastAPI
* Uvicorn

### Frontend

* Python
* Streamlit

### AI & Recommendation

* Natural Language Processing
* Rule-based recommendation engine
* AI itinerary generation

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd hackathon3
```

### 2. Backend Setup

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

The backend will start at:

```
http://127.0.0.1:8000
```

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
```

The frontend will be available at:

```
http://localhost:8501
```

## API Overview

The backend exposes endpoints for:

* Travel preference extraction
* Destination recommendations
* Itinerary generation
* File upload support

## Example Workflow

1. Enter your travel preferences.
2. The AI extracts important travel details.
3. The recommendation engine suggests suitable Hyderabad attractions.
4. A personalized itinerary is generated.
5. Explore the recommended destinations.

## Future Enhancements

* Local guide integration
* Maps and navigation
* Hotel recommendations
* Food recommendations
* Real-time traffic updates
* Budget optimization
* Multi-city support

## Contributing

Contributions are welcome. Please read `CONTRIBUTING.md` before submitting pull requests.

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See the `LICENSE` file for details.
