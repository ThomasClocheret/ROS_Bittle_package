# Documentatie Petoi Robot Hond

# Stap 1 configuratie van de Raspberry Pi

Voor dit project heb ik gebruik gemaakt van de **Raspberry Pi 3 Model A+** 

Deze zal eerst geconfigureerd moeten worden. De enige mogelijkheid is om ROS te draaien op dit specifieke raspberry model is met de Debian buster OS. 

Want Noetic support alleen buster (Debian 10).

> (Omdat mijn Raspberry-camera module niet samenwerkt met de Debian Buster-versie, heb ik zelfs geprobeerd een andere versie van Ubuntu te installeren die dit wel kan. Ik probeerde het te laten werken met behulp van Docker en het uitvoeren ROS in een Docker-container, maar helaas zonder succes.)
> 

 
Om van start te gaan heb ik gebruik gemaakt van de Raspberry Pi Imager, deze staat toe om aan de hand van de Imager een image te builden en op voorhand de username, password en zelfs wifi instellingen mee te geven in de Raspberry image.

Zodra de image succesvol is geïnstalleerd op de Raspberry Pi, kun je verdergaan met het installeren van ROS op het apparaat. [Deze](https://varhowto.com/install-ros-noetic-raspberry-pi-4/) documentatie kan je hierbij helpen. Tijdens het volgen van deze documentatie ondervond ik echter beperkte geheugenproblemen op mijn Raspberry Pi. Dit kan voor problemen zorgen. Gelukkig kunnen we dit probleem oplossen door gebruik te maken van swap-bestanden en het geheugen naar onze SSD weg te schrijven. Je kunt de volgende stappen volgen om dit probleem op te lossen:

1. Open a terminal on your Raspberry Pi or connect to it remotely using SSH.
2. Check the current swap usage by running the following command:
    
    ```bash
    sudo swapon --show
    ```
    
3. If there is no existing swap partition, you'll see no output. In that case, proceed to the next step. If there is already an active swap partition, you'll need to disable it before proceeding. Run the following command to turn off the swap:
    
    ```bash
    sudo swapoff -a
    ```
    
4. Create a new swap file. Determine the desired size for your swap file (e.g., 1GB, 2GB, etc.). The size of the swap file should depend on your specific requirements and available disk space. For example, to create a 1GB swap file, run the following command:
    
    ```bash
    sudo fallocate -l 1G /swapfile
    ```
    
5. Set appropriate permissions for the swap file:
    
    ```bash
    sudo chmod 600 /swapfile
    ```
    
6. Set up the swap area by formatting the file as swap:
    
    ```bash
    sudo mkswap /swapfile
    ```
    
7. Enable the newly created swap file:
    
    ```bash
    sudo swapon /swapfile
    ```
    
8. To make the swap file permanent, you need to add an entry to the `/etc/fstab` file. Open the file with a text editor:
    
    ```bash
    sudo nano /etc/fstab
    ```
    
9. Add the following line to the end of the file:
    
    ```bash
    /swapfile swap swap defaults 0 0
    ```
    
10. Save the changes and exit the text editor.
11. Finally, verify that the new swap space is active by running the following command:
    
    ```bash
    sudo swapon --show
    ```
    

Na een sucesvolle instalatie van ROS is het de bedoeling dat in de raspi-config het seriele gedeelde te enablenen. Deze kan nagekeken worden via via deze [tool](https://tp4348.medium.com/serial-to-raspberry-pi-da635122b4d0).

Als ook dit ingested is kunnen we de onze ROS package code downloaden op zowel de server als de Raspberry Pi. Volg vervolgens de classic ROS commando’s om van de package gebruik te maken.
Deze package kan hier gedownload worden: https://github.com/ThomasClocheret/ROS_Bittle_package.git

> Vergeet niet om gebruik te maken van je eigen model en de bittle_sender_hands_recog.py file aan te passen aan jouw unieke commando’s voor gebruik.
> 

# Stap 1 configuratie van de Arduino

Om de arduino te laten communiseren met de rasberri pi is er een update nodig van de code op het bordje. Dit kan gedaan worden aan de hand van [Arduino IDE](https://www.arduino.cc/en/software). De code kan op mijn GitHub Repo gevonden worden. Als board kan je Arduino Uno selecteren en de huidige USB port waarmee je verbonden bent. Vervolgens enkel op de upload knop duwen om up te loaden.

Via de serials monitor van Arduino IDE kan je ook gebruik maken van de serial monitor. Deze laat toe om via de juiste braud messages te sturen naar de robot om bepaalde acties te testen.

# Stap 3 AI code voor hand herkenning

De code in de AI folder bestaat uit verschillende files met elke een eigen taak.

1. Eerst gebruiken we de  get_image.py file om een dataset te maken.
We veranderen telkens de class name in de code in de naam die we willen voor een bepaalde herkenning. Maak verschillende classes (minstens 2) zodat de AI kan vergelijken.
2. Vervolgens maken gebruik van het get_data.py script om een dataset.csv te maken
3. Vervolgens gaan we de data trainen met een jupiter notebook file, die zorgt voor het maken van ons AI model.
4. En hands_gesture_recog.py laat toe te testen of de model.pkl werkt

# Stap 4 Camera configuratie

Initieel heb ik gebruikgemaakt van de Raspberry Pi Camera V2.1, maar deze bleek niet compatibel te zijn met mijn besturingssysteem. Daarom ben ik, op aanraden van mijn docent, overgeschakeld naar de ESP32-CAM. De ESP32 is een krachtige microcontroller met ingebouwde Wi-Fi- en Bluetooth-mogelijkheden. Dit stelde ons in staat om camerabeelden via Wi-Fi naar onze computer te streamen. Deze beelden konden worden opgevangen en verwerkt door onze AI-logica. De cameramodule werd van stroom voorzien via de USB-verbinding van de Raspberry Pi.