# Spara, importera och synkronisera Flatpak-appar

Med Spara skrivbord kan du spara, importera och synkronisera Flatpak-applikationer tillsammans med deras användardata, utöver ikoner, teman, inställningar och tillägg.

## Var kan jag hitta detta?

Flatpak-relaterade alternativ finns i dialogrutan **Välj konfigurationsobjekt**.
Du kan öppna den från huvudmenyn (tre punkter i fönstrets titelfält).

## Tillgängliga alternativ

### Lista över installerade Flatpak-appar

Sparar och återställer listan över installerade Flatpak-applikationer.

### Användardata för installerade Flatpak-appar

Tillåter dig inkludera användardata för utvalda Flatpak-applikationer.
Klicka på knappen **">"** för att välja vilka appar som ska få sina data sparade.

### Behåll installerade Flatpak-appar och data (aktiverat som standard)

När det är aktiverat kommer Spara skrivbord **INTE att ta bort Flatpak-applikationer eller deras data som inte finns i arkivet**.

När det är inaktiverat kommer Spara skrivbord **att ta bort alla installerade Flatpak-appar som inte listas i det importerade arkivet – inklusive deras användardata**.

⚠️ **Varning:**
Inaktivera endast det här alternativet om du avsiktligt vill att ditt system ska matcha det importerade arkivet exakt. Borttagna program och deras data **kan inte återställas**.

## Hur fungerar import?

Efter att du har valt ett arkiv eller en mapp blir du tillfrågad vilka konfigurationsobjekt som ska importeras.
Klicka på **Verkställ** för att starta importprocessen.

Importordning:

1. Skrivbordskonfiguration (ikoner, teman, teckensnitt, tillägg, inställningar etc.)
2. Flatpak-applikationer och deras användardata (efter nästa inloggning)

Installation och borttagning av Flatpak börjar **efter att du har loggat in i systemet igen**.

### Synkroniseringsläge

I synkroniseringsläge bearbetas Flatpak-applikationer **omedelbart efter att synkroniseringen är klar** (ingen omloggning krävs).

## Viktig anmärkning

Om **Behåll installerade Flatpak-appar och data** är inaktiverat och du har Flatpak-applikationer installerade som inte ingår i det importerade arkivet, kommer de att **tas bort permanent tillsammans med deras användardata**.

{% include footer.html %}