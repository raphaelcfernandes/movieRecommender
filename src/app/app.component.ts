import { Component, OnInit, ViewChild } from '@angular/core';
import { MoviesService } from '../services/movies.service';
import { Movie } from '../models/movie';
import { MatPaginator, MatSort, MatTableDataSource } from '@angular/material';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {
  Movies: Movie[];
  dataSource: MatTableDataSource<Movie>;
  moviesChosen: MatTableDataSource<Movie>;
  private movieArray: Movie[] = [];
  private ratings: number[] = [5, 4, 3, 2, 1, 0];
  private recommendedMovies: [] = [];
  displayedColumns: string[] = ['movieId', 'title', 'year', 'rate', 'select'];
  displayedSelectedMoviesColumns: string[] = ['title', 'year', 'rating', 'actions'];
  isLoadingResults = true;
  rate = new FormControl();

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatPaginator) paginatorMoviesChosen: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  ngOnInit() { }

  constructor(private movieService: MoviesService) {
    this.getAllMovies();
    this.moviesChosen = new MatTableDataSource(this.movieArray);
    this.moviesChosen.paginator = this.paginatorMoviesChosen;
  }

  getAllMovies() {
    return this.movieService.getAllMovies().subscribe(movies => {
      this.Movies = movies as Movie[];
      this.dataSource = new MatTableDataSource(this.Movies);
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
      this.isLoadingResults = false;
    });
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }

  }

  sendRec() {
    this.movieService.sendRecommendation(this.movieArray).subscribe(res => {
      this.recommendedMovies = res.reverse();
    });
  }

  movieChosen(element: Movie) {
    const k = new Movie(element);
    return this.movieArray.find(i => i._Id === k._Id);
  }

  removeMovie(movie: Movie) {
    this.movieArray = this.movieArray.filter(obj => obj !== movie);
    this.moviesChosen = new MatTableDataSource(this.movieArray);
  }

  giveRecommendationToSingleMovie(element: Movie, event) {
    element.Rating = event.value;
  }

  selectMovie(movie: Movie): void {
    const y = new Movie(movie);
    y.Rating = Number(movie.Rating);
    this.movieArray.push(y);
    this.moviesChosen = new MatTableDataSource(this.movieArray);
  }
}
