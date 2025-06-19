const API_BASE = process.env.NEXT_PUBLIC_API_URL;

export const API_ROUTES = {
  // Auth
  LOGIN: `${API_BASE}/login/`,
  REGISTER: `${API_BASE}/register/`,
  REFRESH: `${API_BASE}/token/refresh/`,
  LOGOUT: `${API_BASE}/logout/`,

  // Users
  USERS: `${API_BASE}/users/`,
  ME: `${API_BASE}/users/me/`,

  // Circuits
  CIRCUITS: `${API_BASE}/circuits/`,
  CIRCUIT_DETAIL: (id: number) => `${API_BASE}/circuits/${id}/`,
  CIRCUIT_FILTER: `${API_BASE}/circuits/search/`,
  TAGS: `${API_BASE}/circuits/tags/`,
  CATEGORIES: `${API_BASE}/circuits/categories/`,

  // Bookings
  BOOK: `${API_BASE}/bookings/book/`,
  BOOKINGS: `${API_BASE}/bookings/`,
  MY_BOOKINGS: `${API_BASE}/me/bookings/`,
  BOOKING_DETAIL: (id: number) => `${API_BASE}/bookings/${id}/`,

  // Cart
  CART_MY: `${API_BASE}/carts/my/`,
  CART: `${API_BASE}/carts/`,

  // Payments
  PAYMENTS: `${API_BASE}/payments/`,
  PAYMENT_DETAIL: (id: number) => `${API_BASE}/payments/${id}/`,
  PAYMENT_VALIDATE: (id: number) => `${API_BASE}/payments/${id}/validate/`,

  // Reviews
  REVIEWS: `${API_BASE}/reviews/`,
};
