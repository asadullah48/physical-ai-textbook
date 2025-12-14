/**
 * Real API client - replaces mock implementation
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Module {
  slug: string;
  title: string;
  icon: string;
  description: string;
  chapter_count: number;
  difficulty?: string;
}

export interface Chapter {
  id: string;
  title: string;
  content: string;
  metadata: {
    learning_objectives?: string[];
    skills?: string[];
    [key: string]: any;
  };
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  message: string;
  conversation_history?: ChatMessage[];
  mode?: 'helpful' | 'socratic' | 'embodiment';
  module_filter?: string;
  reading_context?: {
    module_id: string;
    chapter_id: string;
    content: string;
  };
}

export interface ChatResponse {
  response: string;
  sources: Array<{
    title: string;
    module: string;
    section?: string;
    score: number;
  }>;
  mode: string;
  teaching_move?: string;
  robot_state?: {
    capabilities: Record<string, boolean>;
    understanding: Record<string, number>;
    mood: string;
    progress_percentage: number;
  };
}

export interface SkillGraph {
  nodes: Array<{
    id: string;
    label: string;
    module: string;
  }>;
  edges: Array<{
    from: string;
    to: string;
  }>;
}

class APIClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;

    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `API error: ${response.status}`);
    }

    return response.json();
  }

  // ========== Health ==========
  async health(): Promise<{
    status: string;
    rag_ready: boolean;
    socratic_ready: boolean;
    embodiment_ready: boolean;
  }> {
    return this.request('/api/health');
  }

  // ========== Modules ==========
  async getModules(): Promise<Module[]> {
    return this.request('/api/v1/modules');
  }

  async getModuleChapters(moduleId: string): Promise<Chapter[]> {
    return this.request(`/api/v1/modules/${moduleId}/chapters`);
  }

  async getChapter(moduleId: string, chapterId: string): Promise<Chapter> {
    return this.request(`/api/v1/modules/${moduleId}/chapters/${chapterId}`);
  }

  async getSkillGraph(): Promise<SkillGraph> {
    return this.request('/api/v1/skill-graph');
  }

  // ========== Chat ==========
  async chat(request: ChatRequest): Promise<ChatResponse> {
    return this.request('/api/v1/chat', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // ========== Embodiment Mode ==========
  async embodimentReact(chapterMetadata: {
    module_id: string;
    file: string;
    title: string;
  }): Promise<{
    narration: string;
    state_change: Record<string, any>;
    persona: string;
    mood: string;
  }> {
    return this.request('/api/v1/embodiment/react', {
      method: 'POST',
      body: JSON.stringify(chapterMetadata),
    });
  }

  async embodimentChallenge(
    challengeType: string,
    context: Record<string, any>
  ): Promise<{
    scenario: string;
    request: string;
    challenge_type: string;
  }> {
    return this.request(
      `/api/v1/embodiment/challenge?challenge_type=${challengeType}`,
      {
        method: 'POST',
        body: JSON.stringify(context),
      }
    );
  }

  async getRobotState(): Promise<{
    capabilities: Record<string, boolean>;
    understanding: Record<string, number>;
    mood: string;
    progress_percentage: number;
  }> {
    return this.request('/api/v1/embodiment/state');
  }

  // ========== Admin ==========
  async initializeContent(forceReindex: boolean = false): Promise<{
    status: string;
    message: string;
  }> {
    return this.request('/api/v1/admin/initialize', {
      method: 'POST',
      body: JSON.stringify({ force_reindex: forceReindex }),
    });
  }

  // ========== Convenience Methods ==========
  content = {
    listModules: () => this.getModules(),
    getChapter: (moduleId: string, chapterId: string) =>
      this.getChapter(moduleId, chapterId),
  };
}

export const api = new APIClient();
