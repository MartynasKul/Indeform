export interface PurchaseData{
    id: number;
    pavadinimas: string;
    vykdytojoPavadinimas: string;
    nuoroda: string;
    data: string;
    terminas: string;
    bvpzKodas: string[];
    skelbimoTipas: string;
}

export interface UserCredentials{
    username: string;
    password: string;
}

export interface AuthState{
    token: string | null;
    isAuthenticated: boolean;
}