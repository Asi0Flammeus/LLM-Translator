class Language:
    def __init__(self, name, code, translation_prompt):
        self.name = name
        self.code = code
        self.translation_prompt = translation_prompt

class SupportedLanguages:
    def __init__(self):
        self.origin_language = None
        self.languages = [
            Language(
                "English", "en",
                "Translate the Technical Content to English\n"
                "Original Language: {self.origin_language}\n"
                "Content Nature: The material is of a technical nature and may contain industry-specific terms.\n"
                "Links & Technical Words: Do not translate link paths, and highly specific technical words. When in doubt, keep the original term.\n"
                "Formatting: Ensure the output retains the same markdown layout and formatting as the original text. Consistency is paramount.\n"
                "Cultural References: If there are any cultural or context-specific references that do not translate well directly, please paraphrase to retain the intended meaning or provide a brief explanation.\n"
                "---\n"
                "Original Text:\n"
            ),

            Language(
                "German", "de",
                "Technischen Inhalt ins Deutsche übersetzen\n"
                "Ursprungssprache: {self.origin_language}\n"
                "Inhaltsart: Das Material ist technischer Natur und kann branchenspezifische Begriffe enthalten.\n"
                "Links & Fachwörter: Pfadlinks und hochspezifische technische Wörter nicht übersetzen. Im Zweifelsfall den Originalbegriff beibehalten.\n"
                "Formatierung: Stellen Sie sicher, dass das Ergebnis dasselbe Markdown-Layout und dieselbe Formatierung wie der ursprüngliche Text beibehält. Konsistenz ist von größter Bedeutung.\n"
                "Kulturelle Hinweise: Wenn es kulturelle oder kontextspezifische Hinweise gibt, die sich nicht direkt übersetzen lassen, bitte umschreiben, um die beabsichtigte Bedeutung beizubehalten oder eine kurze Erklärung geben.\n"
                "---\n"
                "Originaltext:\n"
            ),

            Language(
                "Spanish", "es",
                "Traduce el Contenido Técnico al Español\n"
                "Idioma Original: {self.origin_language}\n"
                "Naturaleza del Contenido: El material es de naturaleza técnica y puede contener términos específicos de la industria.\n"
                "Enlaces y Palabras Técnicas: No traduzcas los enlaces de ruta ni palabras técnicas altamente específicas. En caso de duda, mantén el término original.\n"
                "Formato: Asegúrate de que la salida mantenga el mismo diseño y formato de Markdown que el texto original. La consistencia es primordial.\n"
                "Referencias Culturales: Si hay referencias culturales o específicas del contexto que no se traduzcan directamente bien, por favor parafrasea para retener el significado previsto o proporciona una breve explicación.\n"
                "---\n"
                "Texto Original:\n"
            ),

            Language(
                "Italian", "it",
                "Traduci il Contenuto Tecnico in Italiano\n"
                "Lingua Originale: {self.origin_language}\n"
                "Natura del Contenuto: Il materiale è di natura tecnica e può contenere termini specifici dell'industria.\n"
                "Link & Parole Tecniche: Non tradurre i link dei percorsi e parole tecniche altamente specifiche. In caso di dubbio, conserva il termine originale.\n"
                "Formattazione: Assicurati che l'output mantenga lo stesso layout e formattazione Markdown del testo originale. La coerenza è fondamentale.\n"
                "Riferimenti Culturali: Se ci sono riferimenti culturali o specifici del contesto che non si traducono bene direttamente, parafrasa per conservare il significato inteso o fornisci una breve spiegazione.\n"
                "---\n"
                "Testo Originale:\n"
            ),

            Language(
                "Portuguese", "pt",
                "Traduzir o Conteúdo Técnico para o Português\n"
                "Língua Original: {self.origin_language}\n"
                "Natureza do Conteúdo: O material é de natureza técnica e pode conter termos específicos da indústria.\n"
                "Links & Palavras Técnicas: Não traduza links de caminho e palavras técnicas altamente específicas. Em caso de dúvida, mantenha o termo original.\n"
                "Formatação: Garanta que a saída mantenha o mesmo layout e formatação Markdown do texto original. A consistência é primordial.\n"
                "Referências Culturais: Se houver referências culturais ou específicas ao contexto que não se traduzam diretamente, parafraseie para reter o significado pretendido ou forneça uma breve explicação.\n"
                "---\n"
                "Texto Original:\n"
            ),

            Language(
                "French", "fr",
                "Traduire le Contenu Technique en Français\n"
                "Langue d'Origine: {self.origin_language}\n"
                "Nature du Contenu: Le matériel est de nature technique et peut contenir des termes spécifiques à l'industrie.\n"
                "Liens & Mots Techniques: Ne pas traduire les liens ni les mots techniques hautement spécifiques. En cas de doute, conservez le terme original.\n"
                "Formatage: Assurez-vous que la sortie conserve le même format et la même mise en page Markdown que le texte original. La cohérence est primordiale.\n"
                "Références Culturelles: Si des références culturelles ou contextuelles ne se traduisent pas bien directement, paraphrasez pour conserver le sens prévu ou fournissez une brève explication.\n"
                "---\n"
                "Texte Original:\n"
            )]



    def set_origin_language_to(self, origin_language):
        self.origin_language = origin_language

    def get_translation_prompt_for_destination(self, destination_language):
        for language in self.languages:
            if language.name == destination_language:
                return language.translation_prompt.format(self=self)

