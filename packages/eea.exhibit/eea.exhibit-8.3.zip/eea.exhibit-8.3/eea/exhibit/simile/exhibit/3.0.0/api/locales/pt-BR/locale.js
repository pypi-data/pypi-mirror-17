/* jslint:disable */
Exhibit.Localization.importLocale("en", {
    "%general.missingLabel": "faltando",
    "%general.missingSortKey": "(faltando)",
    "%general.notApplicableSortKey": "(n/a)",
    "%general.itemLinkLabel": "link",
    "%general.busyIndicatorMessage": " Aguarde...",
    "%general.showDocumentationMessage": "%1$s\n\nWe will show the relevant documentation after this message.",
    "%general.showJavascriptValidationMessage": "We will explain the error in details after this message.",
    "%general.showJsonValidationMessage": "%1$s\n\nWe will explain the error in details after this message.",
    "%general.showJsonValidationFormMessage": "We will browse to a web service where you can upload and check your code after this message.",
    "%general.badJsonMessage": "The JSON data file\n  %1$s\ncontains errors =\n\n%2$s",
    "%general.failedToLoadDataFileMessage": "We cannot locate the data file\n  %1$s\nCheck that the file name is correct.",
    "%general.error.disposeCollection": "Failed to dispose of collection",
    "%general.error.cannotRegister": "Cannot register component %1$s --",
    "%general.error.componentNameTaken": "another component has taken that name",
    "%general.error.noComponentObject": "%1$s no component object provided",
    "%general.error.missingCreateFunction": "%1$s component has no create function",
    "%general.error.missingDOMCreateFunction": "%1$s component has no createFromDOM function",
    "%general.error.unknownViewClass": "Unknown viewClass: %1$s",
    "%general.error.unknownFacetClass": "Unknown facetClass: %1$s",
    "%general.error.unknownCoderClass": "Unknown coderClass: %1$s",
    "%general.error.unknownClass": "Unknown class: %1$s",
    "%general.error.unknownLensType": "Unknown Exhibit.UI.showItemInPopup opts.lensType: %1$s",
    "%general.error.lensSelectorNotFunction": "lensSelector is not a function",
    "%general.error.lensSelectorExpressionNotFunction": "lensSelector expression %1$s is not a function",
    "%general.error.badLensSelectorExpression": "Bad lensSelector expression: %1$s",

    "%lens.error.unknownLensType": "Unknown lens type: %1$s",
    "%lens.error.failedToLoad": "Failed to load view template from %1$s\n%2$s",
    "%lens.error.constructingTemplate": "Lens: Error constructing lens template in job queue",
    "%lens.error.compilingTemplate": "Lens: Error compiling lens template and processing template job queue",
    "%lens.error.misplacedAcceptChanges": "accept-changes element in non-submission item",

    "%registry.error.noSuchRegistry": "No such registry for component: %1$s",

    "%datetime.error.invalidDate": "Invalid date string: %1$s",
    "%datetime.error.invalidTime": "Invalid time string: %1$s",

    "%settings.error.inconsistentDimensions": "Expected a tuple of %1$d dimensions separated with %2$s but got %3$s",
    "%settings.error.notFloatingPoint": "Expected a floating point number but got %1$s",
    "%settings.error.notInteger": "Expected an integer but got %1$s",
    "%settings.error.notBoolean": "Expected either 'true' or 'false' but got %1$s",
    "%settings.error.notFunction": "Expected a function or the name of a function but got %1$s",
    "%settings.error.notEnumerated": "Expected one of %1$s but got %2$s",
    "%settings.error.unknownSetting": "Unknown setting type %1$s",

    "%export.exportButtonLabel": "Exportar",
    "%export.exportAllButtonLabel": "Exportar tudo",
    "%export.exportDialogBoxCloseButtonLabel" : "Fechar",
    "%export.exportDialogBoxPrompt": "Copie esse código para sua Área de Transferência da forma usual. Aperte ESC para fechar essa caixa de diálogo.",
    "%export.focusDialogBoxCloseButtonLabel": "Fechar",
    "%export.rdfXmlExporterLabel": "RDF/XML",
    "%export.smwExporterLabel": "Semantic wikitext",
    "%export.exhibitJsonExporterLabel": "Exhibit JSON",
    "%export.tsvExporterLabel": "Arquivo texto com campos separados por Tab (Excel)",
    "%export.htmlExporterLabel": "Gerar HTML dessa visão",
    "%export.bibtexExporterLabel": "BibTeX",

    "%import.couldNotLoad": "Could not load data from %1$s into the database",
    "%import.couldNotParse": "Could not parse %1$s",
    "%import.missingOrFilesystem": "Failed to access %1$s, possibly because the file is missing or because you are accessing your files via filesystem instead of a webserver while using Chrome or IE.  Use a different browser or move your files onto a webserver.",
    "%import.httpError": "Failed to access %1$s (HTTP %2$d)",
    "%import.failedAccess": "Failed to access %1$s%2$s",
    "%import.failedAccessHttpStatus": " (HTTP %1$d)",

    "%database.itemType.label": "Item",
    "%database.itemType.pluralLabel": "Itens",
    "%database.labelProperty.label": "nome",
    "%database.labelProperty.pluralLabel": "nomes",
    "%database.labelProperty.reverseLabel": "nome de",
    "%database.labelProperty.reversePluralLabel": "nomes de",
    "%database.typeProperty.label": "tipo",
    "%database.typeProperty.pluralLabel": "tipos",
    "%database.typeProperty.reverseLabel": "tipo de",
    "%database.typeProperty.reversePluralLabel": "tipos de",
    "%database.uriProperty.label": "URI",
    "%database.uriProperty.pluralLabel": "URIs",
    "%database.uriProperty.reverseLabel": "URI de",
    "%database.uriProperty.reversePuralLabel": "URIS of",
    "%database.sortLabels.text.ascending":  "a - z",
    "%database.sortLabels.text.descending": "z - a",
    "%database.sortLabels.number.ascending":  "menor primeiro",
    "%database.sortLabels.number.descending": "maior primeiro",
    "%database.sortLabels.date.ascending":  "mais recente primeiro",
    "%database.sortLabels.date.descending": "mais antigo primeiro",
    "%database.sortLabels.boolean.ascending":  "falso primeiro",
    "%database.sortLabels.boolean.descending": "verdadeiro primeiro",
    "%database.sortLabels.item.ascending":  "a - z",
    "%database.sortLabels.item.descending": "z - a",
    "%database.reverseLabel": "inverso de %1$s",
    "%database.reversePluralLabel": "inverso de %1$s",
    "%database.error.unloadable": "Could not load data.",
    "%database.error.loadTypesFailure": "Database loading of types failed",
    "%database.error.loadPropertiesFailure": "Database loading of properties failed",
    "%database.error.loadItemsFailure": "Database loading of items failed",
    "%database.error.removeAllStatementsFailure": "Removing all statements from database failed",
    "%database.error.noImporterFailure": "No importer for data of type %1$s",
    "%database.error.itemSyntaxError": "Item entry has no label and no id: %1$s",
    "%database.error.itemMissingLabelFailure": "Cannot add new item containing no label: %1$s",

    "%expression.error.noSuchFunction": "No such function named %1$s",
    "%expression.error.noSuchVariable": "No such variable called %1$s",
    "%expression.error.mustBeForward": "Last path of segment must be forward",
    "%expression.error.missingPropertyID": "Missing property ID at position %1$d",
    "%expression.error.missingFactor": "Missing factor at end of expression",
    "%expression.error.missingParenEnd": "Missing ) to end %1$s at %2$d",
    "%expression.error.missingParenStart": "Missing ( to start %1$s at %2$d",
    "%expression.error.missingParenFunction": "Missing ) after function call %1$s at position %2$d",
    "%expression.error.missingParen": "Missing ) at position %1$d",
    "%expression.error.unexpectedSyntax": "Unexpected text %1$s at position %2$d",
    "%expression.error.unterminatedString": "Unterminated string starting at %1$d",

    "%coders.mixedCaseLabel": "misto",
    "%coders.missingCaseLabel": "ausente",
    "%coders.othersCaseLabel": "outros",
    "%coders.error.configuration": "%1$s: Error processing configuration of coder",

    "%facets.clearSelectionsTooltip": "Limpar seleções",
    "%facets.facetSelectActionTitle": "Selecione %1$s no filtro %2$s",
    "%facets.facetUnselectActionTitle": "Descelecionar %1$s no filtro %2$s",
    "%facets.facetSelectOnlyActionTitle": "Selecionar apenas %1$s in facet %2$s",
    "%facets.facetClearSelectionsActionTitle": "Clear selections in facet %1$s",
    "%facets.facetTextSearchActionTitle": "Busca textual %1$s",
    "%facets.facetClearTextSearchActionTitle": "Limpar busca textual",
    "%facets.missingThisField": "(campo ausente)",
    "%facets.missingLabel": "falta %1$s",
    "%facets.error.configuration": "%1$s: Error processing configuration of facet",
    "%facets.numeric.rangeShort": "%1$d - %2$d",
    "%facets.numeric.rangeWords": "%1$d até %2$d",
    "%facets.alpha.rangeShort": "%1$s - %2$s",
    "%facets.alpha.rangeWords": "%1$s até %2$s",
    "%facets.hierarchical.othersLabel": "(outros)",
    "%facets.hierarchical.rootLabel": "(raiz)",

    "%views.unplottableTemplate": "<a class=\"exhibit-action exhibit-views-unplottableCount\" href=\"#\" id=\"unplottableCountLink\">%1$d %2$s</a> out of <span class=\"exhibit-views-totalCount\">%3$d</span> cannot be plotted.",
    "%views.resultLabel": "resultado",
    "%views.resultsLabel": "resultados",

    "%viewPanel.selectViewActionTitle": "selecione vista %1$s",
    "%viewPanel.missingViewClassMessage": "The specification for one of the views is missing the viewClass field.",
    "%viewPanel.viewClassNotFunctionMessage": "The view class attribute value '%1$s' you have specified\nfor one of the views does not evaluate to a Javascript function.",
    "%viewPanel.badViewClassMessage": "The view class attribute value '%1$s' you have specified\nfor one of the views is not a valid Javascript expression.",
    "%viewPanel.viewSeparator": " &bull; ",
    "%viewPanel.noViewLabel": "[no view label set]",
    "%viewPanel.error.unknownView": "Unknown viewClass: %1$s",
    "%viewPanel.error.failedViewCreate": "Failed to create view %1$s (%2$d)",

    "%TileView.label": "Matriz",
    "%TileView.tooltip": "Ver ítens como uma matriz",

    "%ThumbnailView.label": "Miniaturas",
    "%ThumbnailView.tooltip": "Ver ítens em miniaturas",

    "%TabularView.label": "Tabela",
    "%TabularView.tooltip": "Ver ítens em uma tabela",
    "%TabularView.columnHeaderSortTooltip": "Clique para ordenar por essa coluna",
    "%TabularView.columnHeaderReSortTooltip": "Clique para ordenar de forma inversa",
    "%TabularView.sortColumnAscending": "ordenar crescentemente por %1$s",
    "%TabularView.sortColumnDescending": "ordenar decrescentemente por %1$s",
    "%TabularView.error.configuration": "TabularView: Error processing configuration of tabular view",

    "%orderedViewFrame.removeOrderLabel": "Remover essa ordenação",
    "%orderedViewFrame.sortingControlsTemplate": "sorted by: <span id=\"ordersSpan\"></span>; <a id=\"thenSortByAction\" href=\"#\" class=\"exhibit-action\" title=\"Further sort the items\">then by...</a>",
    "%orderedViewFrame.formatSortActionTitle": "Ordenado por %1$s (%2$s)",
    "%orderedViewFrame.formatRemoveOrderActionTitle": "Remover ordenação por %1$s (%2$s)",
    "%orderedViewFrame.groupedAsSortedOptionLabel": "agrupar como ordenado",
    "%orderedViewFrame.groupAsSortedActionTitle": "agrupar como ordenado",
    "%orderedViewFrame.ungroupAsSortedActionTitle": "desagrupar como ordenado",
    "%orderedViewFrame.showAllActionTitle": "mostrar todos resultados",
    "%orderedViewFrame.dontShowAllActionTitle": "mostrar apenas os primeiros resultados",
    "%orderedViewFrame.formatDontShowAll": "Mostrar apenas os %1$d primeiros resultados",
    "%orderedViewFrame.formatShowAll": "Mostrar todos os %1$d resultados",
    "%orderedViewFrame.pageWindowEllipses": " ... ",
    "%orderedViewFrame.pageSeparator": " &bull; ",
    "%orderedViewFrame.previousPage": "&laquo;&nbsp;Anterior",
    "%orderedViewFrame.nextPage": "Próxima&nbsp;&raquo;",
    "%orderedViewFrame.pagingActionTitle": "Página %1$d",
    "%orderedViewFrame.pagingLinkTooltip": "Ir para página %1$d",
    "%orderedViewFrame.error.orderExpression": "Bad order expression: %1$s",
    "%orderedViewFrame.error.orderObject": "Bad order object: %1$s",
    "%orderedViewFrame.error.possibleOrderExpression": "Bad possible order expression: %1$s",
    "%orderedViewFrame.error.possibleOrderObject": "Bad possible order object: %1$s",

    "%widget.bookmark.tooltip": "Clique para gerar um bookmark (Favorito)",

    "%widget.collectionSummary.resetFiltersLabel": "Limpar todos filtros",
    "%widget.collectionSummary.resetFiltersTooltip": "Limpar todos filtros e ver ítens originais",
    "%widget.collectionSummary.resetActionTitle": "Limpar todos filtros",
    "%widget.collectionSummary.allResultsTemplate": "<span class=\"%1$s\" id=\"resultDescription\"></span>",
    "%widget.collectionSummary.noResultsTemplate": "<span class=\"%1$s\"><span class=\"%2$s\">0</span> resultados</span> (<span id=\"resetActionLink\"></span>)",
    "%widget.collectionSummary.filteredResultsTemplate": "<span class=\"%1$s\" id=\"resultDescription\"></span> filtrado(a)s de <span id=\"originalCountSpan\">0</span> originalmente (<span id=\"resetActionLink\"></span>)",

    "%formatter.listSeparator": ", ",
    "%formatter.listLastSeparator": ", e ",
    "%formatter.listPairSeparator": " e ",
    "%formatter.textEllipsis": "%1$s...",
    "%formatter.booleanTrue": "verdadeiro",
    "%formatter.booleanFalse": "falso",
    "%formatter.currencySymbol": "$",
    "%formatter.currencySymbolPlacement": "first", // "last", "after-sign"
    "%formatter.currencyShowSign": true,
    "%formatter.currencyShowRed": false,
    "%formatter.currencyShowParentheses": false,
    "%formatter.dateTimeDefaultFormat": "EEE, MMM d, yyyy, hh:mm a",
    "%formatter.dateShortFormat": "dd/MM/yy",
    "%formatter.timeShortFormat": "hh:mm a",
    "%formatter.dateTimeShortFormat": "dd/MM/yy hh:mm a",
    "%formatter.dateMediumFormat": "EEE, MMM d, yyyy",
    "%formatter.timeMediumFormat": "hh:mm a",
    "%formatter.dateTimeMediumFormat": "EEE, MMM d, yyyy, hh:mm a",
    "%formatter.dateLongFormat": "EEEE, MMMM d, yyyy",
    "%formatter.timeLongFormat": "HH:mm:ss z",
    "%formatter.dateTimeLongFormat": "EEEE, MMMM d, yyyy, HH:mm:ss z",
    "%formatter.dateFullFormat": "EEEE, MMMM d, yyyy",
    "%formatter.timeFullFormat": "HH:mm:ss.S z",
    "%formatter.dateTimeFullFormat": "EEEE, MMMM d, yyyy G, HH:mm:ss.S z",
    "%formatter.shortDaysOfWeek": [ "Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb" ],
    "%formatter.daysOfWeek": [ "Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado" ],
    "%formatter.shortMonths": [ "Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez" ],
    "%formatter.months": [ "Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"],

    "%formatter.commonEra": "CE",
    "%formatter.beforeCommonEra": "BCE",
    "%formatter.beforeNoon": "am",
    "%formatter.afterNoon": "pm",
    "%formatter.BeforeNoon": "AM",
    "%formatter.AfterNoon": "PM",

    "%format.error.missingNumber": "Missing number at position %1$d",
    "%format.error.missingInteger": "Missing integer at position %1$d",
    "%format.error.missingNonNegativeInteger": "Missing non-negative integer at position %1$d",
    "%format.error.missingString": "Missing string at position %1$d",
    "%format.error.missingURL": "Missing url at position %1$d",
    "%format.error.missingExpression": "Missing expression at position %1$d",
    "%format.error.missingExpressionOrString": "Missing expression or string at position %1$d",
    "%format.error.missingOption": "Missing option at position %1$d",
    "%format.error.unsupportedOption": "Unsupported option %1$s for setting %2$s on value type %3$s found at position %4$d",
    "%format.error.unsupportedFlag": "Unsupported flag %1$s for setting %2$s on value type %3$s found at position %4$d",
    "%format.error.unsupportedSetting": "Unsupported setting called %1$s for value type %2$s found at position %3$d",
    "%format.error.missingColon": "Missing : at position %1$d",
    "%format.error.missingValueType": "Missing value type at position %1$d",
    "%format.error.unsupportedValueType": "Unsupported value type %1$s at position %2$d",
    "%format.error.missingBrace": "Missing } at position %1$d",
    "%format.error.unterminatedString": "Unterminated string starting at %1$d",
    "%format.error.missingCloseURL": "Missing ) to close url at %1$d"
});
