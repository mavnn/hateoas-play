import { Component, OnInit } from '@angular/core';
import { Http } from '@angular/http';
import { User } from './user';
import { Root } from './root';
import { ApiError } from './api_error';
import { LoginDetails } from './login_details';
import { Timeline } from './timeline';
import { TimelineEvent } from './timelineevent';
import { ApiService } from './api.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css'],
    providers: [ApiService]
})

export class AppComponent implements OnInit {
    constructor(private apiService : ApiService) { }
    title = 'stuff';
    user : User = {
        email : null,
        name : null
    };
    loginUrl : string;
    loginDetails : LoginDetails = {
        'username': null,
        'password': null
    };
    timelines : Timeline [] = [];
    newTimelineTitle : string;
    newTimelineUrl : string;
    selectedTimeline : Timeline;
    timelineEvents : TimelineEvent [] = [];
    showLogin : boolean = false;
    fatalError : ApiError;
    tryLogin(): void {
        this.showLogin = false;
        this.apiService.post<LoginDetails, Root>(this.loginUrl, this.loginDetails)
            .then(this.onRoot.bind(this))
            .catch(this.onRootError.bind(this));
        this.loginDetails = {
            username: null,
            password: null
        };
    }
    newTimeline(): void {
        this.apiService.post<string, Timeline []>(this.newTimelineUrl, this.newTimelineTitle)
            .then(timelines => this.timelines = timelines)
            .catch(e => this.fatalError = e);
    }
    onTimelineSelected(t : Timeline) : void {
        this.selectedTimeline = t;
    }
    onRoot(root : Root) : void {
        this.user = root.user;
        const timelinesUrl = root.links.find(l => l.rel === 'timeline.list');
        const timelineEventsUrl = root.links.find(l => l.rel === 'timelineEvents.list');
        this.newTimelineUrl = root.links.find(l => l.rel === 'timeline.add').href;
        this.apiService.get<Timeline []>(timelinesUrl.href)
            .then(timelines => this.timelines = timelines)
            .catch(e => this.fatalError = e);
        this.apiService.get<TimelineEvent []>(timelineEventsUrl.href)
            .then(timelineEvents => this.timelineEvents = timelineEvents)
            .catch(e => this.fatalError = e);
    };
    onRootError(error : ApiError) : void {
        if (error.error_code === 403) {
            this.loginUrl = error.links.find(l => l.rel === "login").href;
            this.showLogin = true;
        } else {
            this.fatalError = error;
        }
    }
    getRoot(): void {
        this.apiService.getRoot().then(this.onRoot.bind(this)).catch(this.onRootError.bind(this));
    }
    ngOnInit(): void {
        this.getRoot();
    }
}

