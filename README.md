# Gestionnaire de règles iptables avec Flask et TailwindCSS

Ce projet est une application web simple pour gérer les règles iptables sur un serveur Linux.  
Elle permet d'ajouter des règles de filtrage (ACCEPT/DROP) basées sur IP ou nom de domaine, protocole, port simple ou plage, avec une interface utilisateur moderne grâce à TailwindCSS.

---

## Fonctionnalités

- Ajouter des règles iptables pour INPUT ou OUTPUT  
- Supporte les protocoles TCP, UDP, ICMP (ICMP sans port)  
- Ports simples ou plages de ports (uniquement pour TCP/UDP)  
- Résolution DNS pour nom de domaine  
- Suppression automatique des règles similaires avant ajout  
- Affichage des règles iptables actuelles dans l'interface  
- Interface utilisateur moderne et responsive avec TailwindCSS  
- Messages d’erreur et de succès clairs  

---

## Prérequis

- Python 3.7+  
- Linux avec iptables installé et accès root (exécution des commandes iptables requiert les droits administrateur)  
- Flask  
- Accès au terminal avec droits sudo ou root  

---

## Installation

1. Cloner ce dépôt :

```bash
git clone https://github.com/Nouments/web_firewall.git
cd web_firewall
pip install -r requirements.txt
sudo python app.py
---
