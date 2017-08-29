import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { ApiService } from './api.service';
import { Timeline } from './timeline';
import { TimelineEvent } from './timelineevent';
import { Link } from './link';
import { CreateTimelineEvent } from './create_timeline_event';

@Component({
    selector: 'timeline-detail',
    templateUrl: './timeline-detail.component.html',
    styleUrls: ['./app.component.css'],
    providers: [ApiService]
})

export class TimelineDetailComponent implements OnChanges {
    constructor(private apiService : ApiService) {}
    @Input() timeline : Timeline;
    newEventTitle : string;
    newEventDate : string;
    newEventUrl : string;
    timelineEvents : TimelineEvent [];
    newEvent() : void {
        if(this.newEventTitle && this.newEventDate) {
            this.apiService.post<CreateTimelineEvent, TimelineEvent>(this.timeline.links
                                                                .find(l => l.rel === "timelineEvent.add").href,
                                                                { title: this.newEventTitle, date: this.newEventDate })
                .then(te => { this.timelineEvents.push(te);
                              this.timelineEvents.sort(te => te.date.valueOf()) });
        }
    }
    getEvent(timelineTitle : string, link : Link) : void {
        this.apiService.get<TimelineEvent>(link.href)
            .then(te => { if(this.timeline.title === timelineTitle) { this.timelineEvents.push(te) } });
    };
    getDetails() : void {
        this.apiService.get<Timeline>(this.timeline.links.find(l => l.rel === "self").href)
            .then(details =>
                  { details.links.filter(l => l.rel === "timelineEvent")
                    .forEach(eventLink => this.getEvent(details.title, eventLink)); });
    };
    ngOnChanges(changes : SimpleChanges) {
        this.timelineEvents = [];
        this.getDetails();
    };
}
