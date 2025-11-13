export interface Article {
  id: number;
  title: string;
  slug: string;
  url: string;
  summary?: string;
  content?: string;
  author?: string;
  published_at?: string;
  collected_at: string;
  source_id: number;
  category_id?: number;
  language?: string;
  keywords?: string[];
  entities?: {
    persons: string[];
    organizations: string[];
    locations: string[];
    misc: string[];
  };
  sentiment_score?: number;
  relevance_score?: number;
  quality_score?: number;
  image_url?: string;
  word_count?: number;
  reading_time_minutes?: number;
  tags?: string[];
  is_featured: boolean;
  is_verified: boolean;
  is_archived: boolean;
  // Spiegazioni AI pre-generate (già nel JSON)
  explanation_quick?: string;
  explanation_standard?: string;
  explanation_deep?: string;
}

export interface ArticleList {
  items: Article[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface ArticleSearch {
  query?: string;
  category_id?: number;
  source_id?: number;
  date_from?: string;
  date_to?: string;
  min_quality_score?: number;
  language?: string;
  tags?: string[];
}

