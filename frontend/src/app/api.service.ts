import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';
import { Root } from './root';
import { ApiError } from './api_error';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class ApiService {
    private headers = new Headers({ 'content-type': 'application/json'});
    private rootUrl = 'api'

    constructor(private http : Http) {}

    private handleError(error : ApiError) {
        return Promise.reject(error);
    }

    getRoot() : Promise<Root> {
        return this.http.get(this.rootUrl)
            .toPromise()
            .then(response => response.json() as Root)
            .catch(err => this.handleError(err.json()));
    }

    get<T>(url : string) : Promise<T> {
        return this.http.get(url)
            .toPromise()
            .then(response => response.json() as T)
            .catch(err => this.handleError(err.json()));
    }

    post<Request, Response>(url : string, data : Request) : Promise<Response> {
        return this.http.post(url, data)
            .toPromise()
            .then(response => response.json() as Response)
            .catch(err => this.handleError(err.json()));
    }
}
