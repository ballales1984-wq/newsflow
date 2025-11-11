export interface Source {
  id: number;
  name: string;
  slug: string;
  url: string;
  description?: string;
  source_type: 'rss' | 'api' | 'scraper';
  rss_url?: string;
  api_endpoint?: string;
  language?: string;
  country?: string;
  category?: string;
  is_active: boolean;
  is_verified: boolean;
  last_collected_at?: string;
}

