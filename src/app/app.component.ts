import { Component, OnInit, ViewChild } from '@angular/core';
import { MoviesService } from '../services/movies.service';
import { Movie } from '../models/movie';
import { MatPaginator, MatSort, MatTableDataSource, MatTab, MatTable } from '@angular/material';

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

  displayedColumns: string[] = ['movieId', 'title', 'year', 'select'];
  displayedSelectedMoviesColumns: string[] = ['title', 'year', 'rating', 'actions'];
  isLoadingResults = true;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  ngOnInit() { }

  constructor(private movieService: MoviesService) {
    this.getAllMovies();
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
    this.movieService.sendRecommendation(['teste1', 'teste2']).subscribe(res => {
      console.log(res);
    });
  }

  openDialog() {

  }

  movieChosen(element: Movie) {
    const k = new Movie(element);
    return this.movieArray.find(i => i._Id === k._Id);
  }

  removeMovie(movie: Movie) {
    this.movieArray = this.movieArray.filter(obj => obj !== movie);
    this.moviesChosen = new MatTableDataSource(this.movieArray);
  }

  selectMovie(movie: Movie): void {
    const y = new Movie(movie);
    y.Rating = 4;
    this.movieArray.push(y);

    this.moviesChosen = new MatTableDataSource(this.movieArray);

  }
}
