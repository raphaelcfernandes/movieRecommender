export class Movie {

    private movieId: number;
    private year: number;
    private title: string;
    private genres: Array<string>;

    constructor(rawUser) {
        this.movieId = rawUser.movieId;
        this.year = rawUser.year;
        this.title = rawUser.title;
        this.genres = rawUser.genres;
    }

    public getMovieId(): number {
        return this.movieId;
    }

    public getYear(): number {
        return this.year;
    }

    public getTitle(): string {
        return this.title;
    }
    public getGenres(): Array<string> {
        return this.genres;
    }
}
