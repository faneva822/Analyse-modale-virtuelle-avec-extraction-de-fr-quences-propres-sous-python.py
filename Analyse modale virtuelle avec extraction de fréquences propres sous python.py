import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh
from scipy.signal import find_peaks

# ==========================================
# FONCTION DE SAISIE SÉCURISÉE
# ==========================================
def saisir_valeur(message, min_val=None, max_val=None, type_val=float):
    """Boucle de saisie jusqu'à obtention d'une valeur valide."""
    while True:
        try:
            val = type_val(input(message))
            if min_val is not None and val < min_val:
                print(f"Erreur : La valeur doit être au moins {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Erreur : La valeur ne peut pas dépasser {max_val}.")
                continue
            return val
        except ValueError:
            print("Erreur : Entrée invalide. Veuillez saisir un nombre.")

# ==========================================
# 1. PROPRIETES GENERALES
# ==========================================
print("=== ANALYSE MODALE POUTRE ===")

L = saisir_valeur("Longueur (m) : ", 0.01)
E = saisir_valeur("Module de Young (Pa) : ", 1e6)
rho = saisir_valeur("Masse volumique (kg/m3) : ", 10)
n_noeuds = saisir_valeur("Nombre de noeuds (ex: 40) : ", 5, type_val=int)

# ==========================================
# 2. CHOIX PROFIL
# ==========================================
print("\n=== PROFIL ===")
print("1 Rectangle | 2 Carré | 3 Cercle")
print("4 Tube circulaire | 5 IPE | 6 UPN | 7 Cornière | 8 Tube rect")

choix = int(input("Choix : "))

S = 0
I = 0

plt.figure(figsize=(4,4))

# ===== PROFILS SIMPLES =====
if choix == 1:
    b = float(input("b (m): "))
    h = float(input("h (m): "))
    S = b*h
    I = b*h**3/12
    plt.gca().add_patch(plt.Rectangle((0,0),b,h,fill=False))

elif choix == 2:
    a = float(input("a (m): "))
    S = a*a
    I = a**4/12
    plt.gca().add_patch(plt.Rectangle((0,0),a,a,fill=False))

elif choix == 3:
    D = float(input("D (m): "))
    S = np.pi*(D/2)**2
    I = np.pi*D**4/64
    plt.gca().add_patch(plt.Circle((0,0),D/2,fill=False))

# ===== PROFILS STANDARD =====

elif choix == 4:
    profils = {
        1: ("Tube 50", 0.05, 0.003),
        2: ("Tube 100", 0.1, 0.005),
        3: ("Tube 150", 0.15, 0.006)
    }
    for k,v in profils.items():
        print(f"{k} - {v[0]} (D={v[1]} m, e={v[2]} m)")
    c = int(input("Choix : "))
    nom, D, e = profils[c]
    d = D-2*e
    S = np.pi/4*(D**2-d**2)
    I = np.pi/64*(D**4-d**4)
    print(nom, D, e)
    plt.gca().add_patch(plt.Circle((0,0),D/2,fill=False))
    plt.gca().add_patch(plt.Circle((0,0),d/2,fill=False))

elif choix == 5:
    profils = {
        1: ("IPE 100", 0.1, 0.055, 0.0041, 0.0057),
        2: ("IPE 200", 0.2, 0.1, 0.0056, 0.0085),
        3: ("IPE 300", 0.3, 0.15, 0.0065, 0.0107)
    }
    for k,v in profils.items():
        print(f"{k} - {v[0]} (h={v[1]}, b={v[2]})")
    c = int(input("Choix : "))
    nom, h, b, e1, e2 = profils[c]
    S = 2*b*e2+(h-2*e2)*e1
    I = (b*h**3-(b-e1)*(h-2*e2)**3)/12
    print(nom)
    plt.plot([0,b],[0,0])
    plt.plot([0,b],[h,h])
    plt.plot([b/2,b/2],[0,h])

elif choix == 6:
    profils = {
        1: ("UPN 80", 0.08, 0.045, 0.006),
        2: ("UPN 120", 0.12, 0.055, 0.007),
        3: ("UPN 200", 0.2, 0.075, 0.0085)
    }
    for k,v in profils.items():
        print(f"{k} - {v[0]} (h={v[1]}, b={v[2]})")
    c = int(input("Choix : "))
    nom, h, b, e = profils[c]
    S = 2*b*e+(h-e)*e
    I = b*h**3/12
    print(nom)
    plt.plot([0,b],[0,0])
    plt.plot([0,0],[0,h])
    plt.plot([0,b],[h,h])

elif choix == 7:
    profils = {
        1: ("L50x50x5", 0.05, 0.05, 0.005),
        2: ("L80x80x8", 0.08, 0.08, 0.008),
        3: ("L100x100x10", 0.1, 0.1, 0.01)
    }
    for k,v in profils.items():
        print(f"{k} - {v[0]}")
    c = int(input("Choix : "))
    nom, a, b, e = profils[c]
    S = a*e+b*e-e**2
    I = a*b**3/12
    print(nom)
    plt.plot([0,a],[0,0])
    plt.plot([0,0],[0,b])

elif choix == 8:
    profils = {
        1: ("RHS 100x50x4", 0.1, 0.05, 0.004),
        2: ("RHS 150x100x5", 0.15, 0.1, 0.005),
        3: ("RHS 200x100x6", 0.2, 0.1, 0.006)
    }
    for k,v in profils.items():
        print(f"{k} - {v[0]}")
    c = int(input("Choix : "))
    nom, b, h, e = profils[c]
    S = b*h-(b-2*e)*(h-2*e)
    I = (b*h**3-(b-2*e)*(h-2*e)**3)/12
    print(nom)
    plt.gca().add_patch(plt.Rectangle((0,0),b,h,fill=False))
    plt.gca().add_patch(plt.Rectangle((e,e),b-2*e,h-2*e,fill=False))

plt.title("Profil")
plt.axis('equal')
plt.grid()
plt.show()

print("Surface =", S)
print("Inertie =", I)

# ==========================================
# 3. APPUIS
# ==========================================
print("\n1 Encastre | 2 Deux appuis")
choix_appui = int(input("Choix : "))

x = np.linspace(0,L,n_noeuds)

if choix_appui == 1:
    indices = [0,1]
    pos_appuis_reelles = [0.0]
    print("Poutre encastrée configurée à 0.0 m.")
else:
    p1 = float(input("Appui 1 (m): "))
    p2 = float(input("Appui 2 (m): "))
    pos_appuis_reelles = [p1, p2]
    indices = [np.abs(x-p1).argmin(), np.abs(x-p2).argmin()]
    print(f"Appuis positionnés aux noeuds les plus proches des positions {p1}m et {p2}m.")

# ==========================================
# ESQUISSE DE LA POUTRE (Visualisation de contrôle)
# ==========================================
plt.figure(figsize=(10, 3))
plt.plot([0, L], [0, 0], color='gray', lw=6, label="Poutre", zorder=1)

if choix_appui == 1:
    plt.plot([0, 0], [-0.15, 0.15], 'r-', lw=10, label="Encastrement")
else:
    for i, p in enumerate(pos_appuis_reelles):
        plt.plot(p, -0.08, 'r^', markersize=15, label="Appui" if i==0 else "")
        plt.text(p, -0.25, f"{p}m", ha='center', color='red', fontweight='bold')

plt.title("ESQUISSE DE VALIDATION DES APPUIS")
plt.xlim(-L*0.1, L*1.1)
plt.ylim(-0.6, 0.6)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='upper right')
plt.show()

# ==========================================
# 4. MATRICES
# ==========================================
dx = L/(n_noeuds-1)

M = np.eye(n_noeuds)*rho*S*dx
K = np.zeros((n_noeuds,n_noeuds))

k = E*I/dx**3

for i in range(1,n_noeuds-1):
    K[i,i-1:i+2] = k*np.array([-1,2,-1])

K[0,0:2] = k*np.array([1,-1])
K[-1,-2:] = k*np.array([-1,1])

ddl = [i for i in range(n_noeuds) if i not in indices]

K = K[np.ix_(ddl,ddl)]
M = M[np.ix_(ddl,ddl)]

# ==========================================
# 5. ANALYSE MODALE
# ==========================================
eigvals, eigvecs = eigh(K,M)
f_n = np.sqrt(np.abs(eigvals))/(2*np.pi)

print("\n--- FRÉQUENCES PROPRES CALCULÉES ---")
print(f"Fréquence propre fondamentale f1 = {f_n[0]:.3f} Hz")
if len(f_n) > 1:
    print(f"Fréquence propre 2 = {f_n[1]:.3f} Hz")
if len(f_n) > 2:
    print(f"Fréquence propre 3 = {f_n[2]:.3f} Hz")
print("------------------------------------")

# ==========================================
# 6. FRF
# ==========================================
f = np.linspace(1,max(f_n[:3])*1.5,2000)
H = []

eta = 0.02

for freq in f:
    w = 2*np.pi*freq
    Z = K*(1+1j*eta)-w**2*M
    F = np.zeros(len(ddl))
    F[-1]=1
    try:
        X = np.linalg.solve(Z,F)
        H.append(abs(X[-1]))
    except:
        H.append(0)

H = np.array(H)
peaks,_ = find_peaks(H,height=max(H)*0.1)

# ==========================================
# 7. RESULTATS
# ==========================================
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.semilogy(f, H, 'k', label="FRF")
plt.plot(f[peaks], H[peaks], "ro", label="Pics identifiés")
for i, freq in enumerate(f_n[:3]):
    plt.axvline(freq, color=f'C{i+1}', linestyle='--', alpha=0.7,
                label=f"f{i+1} = {freq:.2f} Hz")
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude de la FRF")
plt.title("Fonction de Réponse en Fréquence")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

plt.subplot(1, 2, 2)
mode = np.zeros(n_noeuds)
mode[ddl] = eigvecs[:, 0]
plt.plot(x, mode/max(np.abs(mode)), 'b-', lw=2, label="Mode 1")
plt.axhline(0, color='black', alpha=0.3)
for p in pos_appuis_reelles: plt.plot(p, 0, 'r^', ms=10)
plt.title(f"Premier Mode Propre - f1 = {f_n[0]:.2f} Hz")
plt.xlabel("Position (m)")
plt.ylabel("Déplacement normalisé")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='upper right')

plt.tight_layout()
plt.show()