interface UserPayload {
    id: number;
    email: string;
    username: string;
}

interface DecodedToken {
    exp: number;
    iat: number;
    user?: UserPayload;
}

export function decodeToken(token: string): DecodedToken | null {
    if (!token) return null;
    try {
        const [, payload] = token.split(".");
        if (!payload) return null;
        const decoded = JSON.parse(atob(payload)) as DecodedToken;
        return decoded;
    } catch {
        return null;
    }
}

export function isTokenExpired(token: string): boolean {
    const decoded = decodeToken(token);
    if (!decoded?.exp) return true;
    const currentTime = Math.floor(Date.now() / 1000);
    return decoded.exp < currentTime;
}
