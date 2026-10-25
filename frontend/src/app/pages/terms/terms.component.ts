import { Component, OnInit } from '@angular/core';
import { SeoService } from '../../services/seo.service';

@Component({
  selector: 'app-terms',
  templateUrl: './terms.component.html',
  styleUrls: ['./terms.component.scss']
})
export class TermsComponent implements OnInit {
  currentDate = new Date();

  constructor(private seoService: SeoService) {}

  ngOnInit(): void {
    this.seoService.updateTermsSeo();
  }
}

