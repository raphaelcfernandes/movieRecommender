import { Component, OnInit, ViewChild } from '@angular/core';
import { MoviesService } from '../services/movies.service';
import { Movie } from '../models/movie';
import { MatPaginator, MatSort, MatTableDataSource } from '@angular/material';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {
  Movies: Movie[];
  dataSource: MatTableDataSource<Movie>;
  displayedColumns: string[] = ['movieId', 'title', 'year','select'];

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  ngOnInit() { }

  constructor(private movieService: MoviesService) {
    this.getAllMovies();
  }

  getAllMovies() {
    return this.movieService.getAllMovies().subscribe(movies => {
      this.Movies = movies;
      this.dataSource = new MatTableDataSource(this.Movies);
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    })
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
}
