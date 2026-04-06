import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'stripHtml'
})
export class StripHtmlPipe implements PipeTransform {
  transform(value: string | undefined | null): string {
    if (!value) {
      return '';
    }

    // First decode HTML entities BEFORE removing tags
    let result = value
      // Decode common HTML entities first
      .replace(/&nbsp;/g, ' ')
      .replace(/&amp;/g, '&')
      .replace(/</g, '<')
      .replace(/>/g, '>')
      .replace(/"/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&apos;/g, "'")
      .replace(/&#8217;/g, "'")
      .replace(/&#8216;/g, "'")
      .replace(/&#8220;/g, '"')
      .replace(/&#8221;/g, '"')
      .replace(/&#8230;/g, '...')
      .replace(/&mdash;/g, '—')
      .replace(/&ndash;/g, '–')
      // Decode numeric HTML entities
      .replace(/&#\d+;/g, (match) => {
        return String.fromCharCode(parseInt(match.match(/\d+/)![0], 10));
      });

    // Now remove all HTML tags
    result = result.replace(/<[^>]*>/g, '');

    // Clean up whitespace
    return result.replace(/\s+/g, ' ').trim();
