// Structure du payload décodé depuis le JWT (adapté à SimpleJWT de Django)
export interface DecodedJWT {
  user_id: number;
  email: string;
  username?: string;
  exp: number; // expiration timestamp
  iat?: number;
}

/**
 * Decode a JWT token and return the payload as an object
 */
export function decodeToken(token: string): DecodedJWT | null {
  if (!token) return null;
  try {
    const [, payload] = token.split('.');
    if (!payload) return null;

    // Decode Base64URL → Base64
    const base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = atob(base64);
    const decoded = JSON.parse(jsonPayload) as DecodedJWT;
    return decoded;
  } catch (error) {
    console.error('❌ Failed to decode JWT token:', error);
    return null;
  }
}

/**
 * Check whether a token is expired based on the "exp" claim
 */
export function isTokenExpired(token: string): boolean {
  const decoded = decodeToken(token);
  if (!decoded?.exp) return true;

  const currentTime = Math.floor(Date.now() / 1000); // seconds
  return decoded.exp < currentTime;
}
