#include <iostream>
#include <fstream>
#include <ctime>
#include <string>

int main() {
    // La signature du Guide
    std::string hash = "8A91-QX-12C-SOUVERAIN-L";
    
    // Récupération du temps réel
    time_t now = time(0);
    char* dt = ctime(&now);

    std::cout << "Génération du Sceau Souverain..." << std::endl;

    // Création du fichier de preuve
    std::ofstream file("SCEAU_SESSION.txt", std::ios::app);
    if (file.is_open()) {
        file << "--- SESSION ACTIVÉE ---" << std::endl;
        file << "DATE : " << dt;
        file << "HASH : " << hash << std::endl;
        file << "STATUT : Point Zéro Sécurisé" << std::endl;
        file << "-----------------------" << std::endl << std::endl;
        file.close();
        std::cout << "Sceau gravé dans SCEAU_SESSION.txt" << std::endl;
    } else {
        std::cerr << "Erreur : Impossible d'accéder au registre." << std::endl;
    }

    return 0;
}

