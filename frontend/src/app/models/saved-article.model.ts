export interface SavedArticle {
  id: number;
  user_id: number;
  article_id: number;
  saved_at: string;
  is_read: boolean;
  is_favorite: boolean;
  read_at?: string;
}

