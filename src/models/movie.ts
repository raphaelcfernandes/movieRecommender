export class Movie {

    private movieId: number;
    private year: number;
    private title: string;
    private genres: Array<string>;
    private rating: number;
    private _id: string;

    constructor(rawUser) {
        this.movieId = rawUser.movieId;
        this.year = rawUser.year;
        this.title = rawUser.title;
        this.genres = rawUser.genres;
        this._id = rawUser._id;
        this.rating = rawUser.rate;
    }

    get MovieId(): number {
        return this.movieId;
    }

    get Year(): number {
        return this.year;
    }

    get Title(): string {
        return this.title;
    }

    get Genres(): Array<string> {
        return this.genres;
    }

    get Rating(): number {
        return this.rating;
    }

    get _Id(): string {
        return this._id;
    }

    set Rating(rating: number) {
        this.rating = rating;
    }

}
