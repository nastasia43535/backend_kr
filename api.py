from fastapi import FastAPI, Path, Query, HTTPException
import uvicorn

app = FastAPI()

movies_data = {
    'action': [
        {'title': 'Безумный Макс', 'year': 2015, 'rating': 8.1},
        {'title': 'Джон Уик', 'year': 2014, 'rating': 7.4}
    ],
    'drama': [
        {'title': 'Крестный отец', 'year': 1972, 'rating': 9.2},
        {'title': 'Форрест Гамп', 'year': 1994, 'rating': 8.8}
    ],
    'comedy': [
        {'title': 'Маска', 'year': 1994, 'rating': 6.9},
        {'title': 'Назад в будущее', 'year': 1985, 'rating': 8.5}
    ]
}


@app.get("/movies/{genre}")
def get_movies_by_genre(
        genre: str = Path(..., description="Жанр фильма"),
        min_rating: float = Query(0.0, ge=0.0, le=10.0, description="Минимальный рейтинг"),
        year: int = Query(None, ge=1900, le=2025, description="Год выпуска")
):
    if genre not in movies_data:
        return {"error": "Жанр не найден"}

    movies = movies_data[genre]
    filtered_movies = []

    for movie in movies:
        if movie["rating"] < min_rating:
            continue

        if year is not None and movie["year"] != year:
            continue

        filtered_movies.append(movie)

    return filtered_movies


@app.get("/movies/{genre}/{title}")
def get_movie_by_title(
        genre: str = Path(..., description="Жанр фильма"),
        title: str = Path(..., description="Название фильма")
):
    if genre not in movies_data:
        return {"error": "Жанр не найден"}

    for movie in movies_data[genre]:
        if movie["title"].lower() == title.lower():
            return movie

    raise HTTPException(status_code=404, detail="Фильм не найден")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8007)