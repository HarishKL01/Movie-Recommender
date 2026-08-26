 # 🎬 MovieLens Recommendation App

A lightweight full-stack platform featuring a simple HTML frontend and a robust backend built with Python, FastAPI, and Pandas. This application powers live movie searches, genre listings, and personalized recommendations using the classic MovieLens dataset.

## 🚀 Features

* **HTML Frontend:** A clean, vanilla HTML/JS interface that connects seamlessly to the API without requiring complex build tools.
* **Content-Based Filtering:** Generates recommendations using weighted ratings for a user's favorite genre.


* **Item-Item Collaborative Filtering:** Suggests similar movies using a correlation matrix based on user rating patterns.


* **Live Search Autocomplete:** Features a case-insensitive search endpoint (`/movies/search`) designed to power the frontend autocomplete box.


* **CORS Enabled:** Pre-configured with Cross-Origin Resource Sharing middleware so your HTML frontend can communicate with the backend seamlessly.



## 🛠️ Tech Stack

* **Frontend:** HTML, Vanilla JavaScript, CSS
* **Backend Framework:** FastAPI


* **Data Processing:** Pandas, NumPy


* **Data Validation:** Pydantic



## 📂 Project Structure

```text
├── index.html             # Main HTML frontend interface
├── main.py                # FastAPI application and API routes[cite: 3]
├── recommender.py         # Recommendation logic and Pandas processing[cite: 4]
├── ml-latest-small/       # Data directory (must be created)
│   ├── movies.csv         # Movie metadata[cite: 4]
│   └── ratings.csv        # User ratings[cite: 4]
└── README.md

```

## ⚙️ Installation & Setup

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

```

**2. Install Backend Dependencies**

```bash
pip install fastapi uvicorn pandas numpy pydantic

```

**3. Download the Dataset**

* Download the `ml-latest-small.zip` dataset directly from [GroupLens](https://www.google.com/search?q=https://files.grouplens.org/datasets/movielens/ml-latest-small.zip).


* Extract the contents into a folder named `ml-latest-small` in your project root.


* Ensure `movies.csv` and `ratings.csv` are located directly inside this directory.



**4. Run the Backend Server**

```bash
uvicorn main:app --reload

```

The backend service code will be available at `[http://127.0.0.1:8000](http://127.0.0.1:8000)`[cite: 5].

**5. Launch the Frontend**
Since the frontend is standard HTML, simply double-click the `index.html` file to open it in your web browser. No compilation or frontend server is required!

## 📡 API Reference

The backend exposes the following RESTful routes:

### 1. Get Available Genres

Returns a sorted list of every distinct genre found in the dataset.

* **Endpoint:** `GET /genres`


### 2. Search Movies

Returns the `id` and `title` for up to 10 movies whose titles match the query string.

* **Endpoint:** `GET /movies/search?query={text}`


### 3. Get Recommendations

Accepts a user profile and returns a personalized list of recommendations. Pass either a `favorite_genre` or `favorite_movie` to trigger the respective recommendation engine.

* **Endpoint:** `POST /recommend`

* **Request Body Example:**
```json
{
  "name": "Jane Doe",
  "age": 28,
  "favorite_genre": "Sci-Fi",
  "favorite_movie": null
}



