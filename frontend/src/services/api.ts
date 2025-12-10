const API_URL = 'http://localhost:8000/api/v1';

export interface Module {
  slug: string;
  title: string;
  icon: string;
  description: string;
  chapter_count: number;
}

class APIClient {
  async getModules(): Promise<Module[]> {
    const res = await fetch(`${API_URL}/modules`);
    return res.json();
  }

  async chat(message: string) {
    const res = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
    return res.json();
  }

  content = {
    listModules: async () => this.getModules()
  };
}

export const api = new APIClient();
