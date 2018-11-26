import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Observable } from 'rxjs';
import { startWith, map } from 'rxjs/operators';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MoviesService } from '../services/movies.service';
import { Movie } from '../models/movie';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  myControl = new FormControl();
  options: string[] = ['One', 'Two', 'Three'];
  filteredOptions: Observable<string[]>;
  books: any;
  public Movies: Array<Movie>;

  constructor(private fb: FormBuilder, private movieService: MoviesService) { }

  getAllMovies() {
    this.movieService.getAllMovies().subscribe(movies => {
      this.Movies = movies;
      // console.log(this.Movies)
      this.books = "blablabla";
    })
  }
  ngOnInit() {
    this.filteredOptions = this.myControl.valueChanges
      .pipe(
        startWith(''),
        map(value => this._filter(value))
      );
    this.getAllMovies();
  }
  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();

    return this.options.filter(option => option.toLowerCase().includes(filterValue));
  }

  sendRec() {

    this.movieService.sendRecommendation(['teste1', 'teste2']).subscribe(res => {
      console.log(res);
    });
  }
}
