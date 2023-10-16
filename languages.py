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
                "Instruction: You MUST NOT translate yml property names.\n"
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
                "Anweisung: Sie MÜSSEN die Namen der yml-Eigenschaften NICHT übersetzen.\n"
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
                "Instrucción: NO DEBE traducir los nombres de las propiedades yml.\n"
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
                "Istruzioni: NON si devono tradurre i nomi delle proprietà yml.\n"
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
                "Instrução: NÃO DEVE traduzir nomes de propriedades yml.\n"
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
                "Instruction : Vous NE DEVEZ PAS traduire les noms de propriétés yml.\n"
                "Références Culturelles: Si des références culturelles ou contextuelles ne se traduisent pas bien directement, paraphrasez pour conserver le sens prévu ou fournissez une brève explication.\n"
                "---\n"
                "Texte Original:\n"
            ),

            Language(
                "Swedish", "sv",
                "Översätt det Tekniska Innehållet till Svenska\n"
                "Ursprungsspråk: {self.origin_language}\n"
                "Innehållets Karaktär: Materialet är av teknisk art och kan innehålla branschspecifika termer.\n"
                "Länkar & Tekniska Ord: Översätt inte länkstigar och högspecifika tekniska ord. Vid tvekan, behåll den ursprungliga termen.\n"
                "Formatering: Se till att utfallet behåller samma markdown-layout och formatering som den ursprungliga texten. Konsekvens är av yttersta vikt.\n"
                "Instruktion: Du får INTE översätta yml-egenskapsnamn.\n"
                "Kulturella Referenser: Om det finns kulturella eller sammanhangsspecifika referenser som inte direkt översätts väl, omformulera för att behålla den avsedda meningen eller ge en kort förklaring.\n"
                "---\n"
                "Originaltext:\n"
            ),

            Language(
                "Arabic", "ar",
                "ترجم المحتوى التقني إلى العربية\n"
                "اللغة الأصلية: {self.origin_language}\n"
                "طبيعة المحتوى: المادة ذات طابع تقني وقد تحتوي على مصطلحات خاصة بالصناعة.\n"
                "الروابط والكلمات التقنية: لا تترجم مسارات الروابط والكلمات التقنية المحددة جدًا. في حالة الشك، احتفظ بالمصطلح الأصلي.\n"
                "التنسيق: تأكد من أن الناتج يحتفظ بنفس تنسيق وتخطيط الماركداون كالنص الأصلي. الاتساق أمر بالغ الأهمية.\n"
                "التعليمات: يجب عليك عدم ترجمة أسماء الخصائص في ملف الـ yml.\n"
                "الإشارات الثقافية: إذا كانت هناك إشارات ثقافية أو خاصة بالسياق لا تترجم جيدًا بشكل مباشر، يرجى إعادة صياغتها للاحتفاظ بالمعنى المقصود أو تقديم شرح موجز.\n"
                "---\n"
                "النص الأصلي:\n"
            ),

            Language(
                "Japanese", "ja",
                "技術的な内容を日本語に翻訳する\n"
                "元の言語: {self.origin_language}\n"
                "コンテンツの性質: この資料は技術的な性質を持っており、業界固有の用語を含む場合があります。\n"
                "リンクと技術的な言葉: リンクのパスや非常に専門的な技術用語を翻訳しないでください。疑問の場合は、元の用語をそのまま使用してください。\n"
                "フォーマット: 出力が元のテキストと同じマークダウンのレイアウトとフォーマットを保持するようにしてください。一貫性が極めて重要です。\n"
                "指示：ymlのプロパティ名を翻訳しないでください。\n"
                "文化的な参照: 直接うまく翻訳できない文化的または文脈固有の参照がある場合は、意図された意味を保持するために言い換えるか、簡単な説明を提供してください。\n"
                "---\n"
                "元のテキスト:\n"
            )]



    def set_origin_language_to(self, origin_language):
        self.origin_language = origin_language

    def get_translation_prompt_for_destination(self, destination_language):
        for language in self.languages:
            if language.name == destination_language:
                return language.translation_prompt.format(self=self)

