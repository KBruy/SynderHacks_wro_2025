// Shared types for Sales Optimizer Backend
// These types are the source of truth and should be synced with frontend

export interface ApiResponse<T> {
  data?: T;
  error?: ApiError;
  meta?: PaginationMeta;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
  status: number;
}

export interface PaginationMeta {
  page: number;
  limit: number;
  total: number;
  totalPages?: number;
}

export interface PaginationQuery {
  page?: number;
  limit?: number;
}

// Product related types
export interface ProductFilters {
  rotation?: 'LOW' | 'MEDIUM' | 'HIGH';
  channel?: string;
  q?: string; // search query
  minStock?: number;
  maxStock?: number;
}

// Recommendation related types
export interface RecommendationFilters {
  status?: 'PENDING' | 'APPLIED' | 'REJECTED' | 'EXPIRED';
  type?: string;
  productId?: string;
}

export interface ApplyRecommendationDto {
  actor?: string;
  schedule?: Date | null;
}

// Connector related types
export interface ConnectorCredentials {
  apiKey?: string;
  apiSecret?: string;
  accessToken?: string;
  shop?: string; // for Shopify
  url?: string; // for WooCommerce
  [key: string]: unknown;
}

export interface SyncResult {
  success: boolean;
  itemsProcessed: number;
  itemsTotal: number;
  errors?: string[];
}

export interface PlatformConnector {
  connect(credentials: ConnectorCredentials): Promise<void>;
  disconnect(): Promise<void>;
  syncAll(): Promise<SyncResult>;
  syncProduct(sku: string): Promise<SyncResult>;
  handleWebhook(payload: unknown): Promise<void>;
}

// AI/Analysis types
export interface MarketAnalysis {
  competitivePosition: 'low' | 'medium' | 'high';
  priceRecommendation: {
    suggestedPrice: number;
    reasoning: string;
    expectedImpact: {
      ctrDelta: number;
      crDelta: number;
    };
  };
  otherRecommendations: Array<{
    type: string;
    action: string;
    priority: 'low' | 'medium' | 'high';
    confidence: number;
  }>;
}

export interface PromptContext {
  product?: unknown;
  marketData?: unknown;
  [key: string]: unknown;
}
