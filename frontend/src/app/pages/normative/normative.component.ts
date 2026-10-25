import { Component } from '@angular/core';

@Component({
  selector: 'app-normative',
  templateUrl: './normative.component.html',
  styleUrls: ['./normative.component.scss']
})
export class NormativeComponent {
  currentDate = new Date().toLocaleDateString('it-IT');
}
