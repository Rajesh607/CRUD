export interface User {
  id: number;
  email: string;
  role: "admin" | "analyst";
}

export interface Company {
  id: number;
  company_name: string;
  industry: string;
  country: string;
  revenue: string;
  employees: string;
  website: string;
  executives: string[];
  products_services: string[];
  partners: string[];
  risks: string[];
  source_facts: string[];
  normalized_by: string;
}

export interface Summary {
  company_id: number;
  overview: string;
  key_insights: string[];
  risks: string[];
  important_facts: string[];
}

export interface Relationship {
  id: number;
  links: string[];
  similarities: string[];
  risks: string[];
  opportunities: string[];
  similarity_score: number;
  risk_score: number;
  opportunity_score: number;
  confidence_score: number;
  ai_summary: string;
}
