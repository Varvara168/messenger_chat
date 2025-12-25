// api.js
const API_BASE = "http://localhost:8000";

class ApiClient {
    constructor() {
        this.baseURL = API_BASE;
        this.useCookies = true;  // Используем куки по умолчанию
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const defaultOptions = {
            credentials: this.useCookies ? 'include' : 'omit',
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        };

        // Если есть токен в localStorage и не используем куки
        const token = localStorage.getItem("ACCESS_TOKEN");
        if (token && !this.useCookies) {
            defaultOptions.headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, { ...defaultOptions, ...options });
            
            if (response.status === 401) {
                // Не авторизован
                localStorage.clear();
                window.location.href = "login.html";
                throw new Error("Unauthorized");
            }
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error(`Request failed for ${endpoint}:`, error);
            throw error;
        }
    }

    async login(creds, password) {
        const response = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ creds, password })
        });
        
        // Сохраняем данные пользователя
        if (response.user_id) {
            localStorage.setItem("CURRENT_USER_ID", response.user_id);
            localStorage.setItem("CURRENT_USER_NAME", response.user?.short_name || "Пользователь");
        }
        
        return response;
    }

    async getMe() {
        return this.request('/auth/me');
    }

    async getChats() {
        return this.request('/chat/get_chats');
    }

    async getMessages(chatId, limit = 50, offset = 0) {
        return this.request(`/chat/${chatId}/messages?limit=${limit}&offset=${offset}`);
    }

    async sendMessage(chatId, text) {
        return this.request('/messages/by_user', {
            method: 'POST',
            body: JSON.stringify({ chat_id: chatId, text })
        });
    }
}

// Экспортируем инстанс
const api = new ApiClient();