import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/screens/home/pages/company/info/"
import "qrc:/resources/qml/components/911/" as Custom

Rectangle {
    color: ui.colors.dark3
    height: gridLayout.height
    property var copy: false

    GridLayout {
        id: gridLayout
        columns: 4
        rowSpacing: 4
        columnSpacing: 32
        width: parent.width

        InfoCell {
            id: headerCell
            Layout.columnSpan: 4

            Custom.FontText {
                font.pixelSize: 20
                text: tr.a911_general_info
                color: ui.colors.white
                opacity: 0.5

                anchors {
                    bottom: parent.bottom
                    bottomMargin: 12
                    left: parent.left
                }
            }

            Item {
                id: editItem
                width: 150
                height: 48
                anchors {
                    verticalCenter: parent.verticalCenter
                    right: parent.right
                }
            }
        }

        InfoCell {
            id: fullNameCell
            Layout.columnSpan: 2
            Layout.minimumHeight: fullNameField.height + 24
            Layout.maximumHeight: fullNameField.height + 24

            Custom.TextFieldEdit {
                id: fullNameField
                width: parent.width
                key: tr.a911_full_name + ui.required
                valueText.control.maximumLength: 200
                value: ""
                distance: 12
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }

                Connections {
                    target: app.company_module
                    onSaveCompanyValidationErrors: {
                        if (result["3"]) {
                            fullNameField.valueText.valid = false
                            fullNameField.valueText.error = result["3"].message
                        }
                    }
                }
            }
        }

        InfoCell {
            id: declarationCell
            Layout.columnSpan: 2
            Layout.minimumHeight: declarationField.height + 24
            Layout.maximumHeight: declarationField.height + 24

            Custom.TextFieldEdit {
                id: declarationField
                width: parent.width
                key: tr.a911_state_declaration_number + ui.required
                valueText.control.maximumLength: 100
                value: ""
                distance: 12
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }

                Connections {
                    target: app.company_module
                    onSaveCompanyValidationErrors: {
                        if (result["6"]) {
                            declarationField.valueText.valid = false
                            declarationField.valueText.error = result["6"].message
                        }
                    }
                }
            }
        }

        InfoCell {
            id: shortNameCell
            Layout.columnSpan: 1
            Layout.minimumHeight: shortNameField.height + 24
            Layout.maximumHeight: shortNameField.height + 24

            Custom.TextFieldEdit {
                id: shortNameField
                width: parent.width
                key: tr.a911_short_word + ui.required
                valueText.control.maximumLength: 100
                value: ""
                distance: 12
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }

                Connections {
                    target: app.company_module
                    onSaveCompanyValidationErrors: {
                        if (result["4"]) {
                            shortNameField.valueText.valid = false
                            shortNameField.valueText.error = result["4"].message
                        }
                    }
                }
            }
        }

        InfoCell {
            Layout.columnSpan: 1
        }

        InfoCell {
            id: ceoCell
            Layout.columnSpan: 2
            Layout.minimumHeight: ceoField.height + 24
            Layout.maximumHeight: ceoField.height + 24

            Custom.TextFieldEdit {
                id: ceoField
                width: parent.width
                key: tr.a911_director_fio
                valueText.control.maximumLength: 200
                value: ""
                distance: 12
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }

                Connections {
                    target: app.company_module
                    onSaveCompanyValidationErrors: {
                        if (result["7"]) {
                             ceoField.valueText.valid = false
                             ceoField.valueText.error = result["7"].message
                        }
                    }
                }
            }
        }


        InfoCell {
            id: phoneCell
            Layout.minimumHeight: phoneField.height + 24
            Layout.maximumHeight: phoneField.height + 24

            Custom.TextFieldEdit {
                id: phoneField
                width: parent.width
                key: tr.phone + ui.required
                valueText.control.maximumLength: 30
                valueText.control.validator: RegExpValidator { regExp: /(\+|[0-9])?[0-9]+/ }
                value: ""
                distance: 12
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }

                Connections {
                    target: app.company_module
                    onSaveCompanyValidationErrors: {
                        if (result["20[0].1"]) {
                            phoneField.valueText.valid = false
                            phoneField.valueText.error = result["20[0].1"].message
                        }
                    }
                }
            }
        }

        InfoCell {
            id: emailCell
            Layout.minimumHeight: emailField.height + 24
            Layout.maximumHeight: emailField.height + 24

            Custom.TextFieldEdit {
                id: emailField
                width: parent.width
                key: tr.email + ui.required
                valueText.control.maximumLength: 100
                value: ""
                distance: 12
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }

                Connections {
                    target: app.company_module
                    onSaveCompanyValidationErrors: {
                        if (result["21[0].1"]) {
                            emailField.valueText.valid = false
                            emailField.valueText.error = result["21[0].1"].message
                        }
                    }
                }
            }
        }

        InfoCell {}

        InfoCell {}

        InfoCell {
            id: logoHeaderCell
            Layout.columnSpan: 2

            Rectangle {
                height: 1
                color: ui.colors.white
                opacity: 0.1
                anchors {
                    top: parent.top
                    left: parent.left
                    right: parent.right
                }
            }

            Custom.FontText {
                font.pixelSize: 20
                text: tr.a911_logo
                color: ui.colors.white
                opacity: 0.5

                anchors {
                    bottom: parent.bottom
                    bottomMargin: 12
                    left: parent.left
                }
            }
        }

        InfoCell {
            id: infoHeaderCell
            Layout.columnSpan: 2

            Rectangle {
                height: 1
                color: ui.colors.white
                opacity: 0.1
                anchors {
                    top: parent.top
                    left: parent.left
                    right: parent.right
                }
            }

            Custom.FontText {
                font.pixelSize: 20
                text: tr.a911_services_provided
                color: ui.colors.white
                opacity: 0.5

                anchors {
                    bottom: parent.bottom
                    bottomMargin: 12
                    left: parent.left
                }
            }
        }

        InfoCell {
            id: logoCell
            Layout.minimumHeight: 128
            Layout.maximumHeight: 128
            Layout.columnSpan: 2
            property var tempLogoImg: ''
            property var imageId: ''
            Canvas {
                id: canvas
                width: 128
                height: 128
                Rectangle {
                    width: 16
                    height: 16
                    radius: height / 2
                    anchors.centerIn: parent
                    color: canvas.colorChange ? ui.colors.blue1 : ui.colors.dark1
                }
                property var colorChange: false
                property int lineWidth: 3
                visible: backgroundDropArea.emptyImage
                function clear() {
                    var ctx = getContext("2d")
                    ctx.reset()
                    canvas.requestPaint()
                }
                function enterArea() {
                    canvas.clear()
                    canvas.colorChange = true
                    canvas.requestPaint()
                }
                function exitArea() {
                    canvas.clear()
                    canvas.colorChange = false
                    canvas.requestPaint()
                }
                onPaint: {
                    var ctx = canvas.getContext("2d")
                    ctx.setLineDash([4, 4])
                    ctx.strokeStyle = colorChange ? ui.colors.blue1 : ui.colors.dark1
                    ctx.lineWidth = lineWidth
                    ctx.beginPath()
                    ctx.roundedRect(0, 0, 128, 128, 6, 6)
                    ctx.stroke()
                }
            }
            Rectangle {
                id: backgroundDropArea
                width: 128
                height: 128
                color: "transparent"
                radius: 6
                property var emptyImage: editLogoCompany.source == ""
                property var deletedImage: false

                Connections {
                    target: app.company_module
                    onUploadCompanyLogoSuccess: {
                         logoCell.tempLogoImg = logo_url
                         logoCell.imageId = image_id
                    }
                }

                Image {
                    id: editLogoCompany
                    anchors.fill: parent
                    sourceSize.width: 128
                    sourceSize.height: 128
                    source: {
                        if (backgroundDropArea.deletedImage) return ""
                        if (logoCell.tempLogoImg) return logoCell.tempLogoImg
                        return ""
                    }
                    Custom.DeleteIcon {
                        id: deleteIcon
                        img.sourceSize.width: 40
                        img.sourceSize.height: 40
                        visible: !backgroundDropArea.deletedImage && logoCell.tempLogoImg
                        anchors {
                            top: parent.top
                            right: parent.right
                        }
                    }
                     Custom.HandMouseArea  {
                        anchors.fill: editLogoCompany
                        onClicked: {
                            fileDialogCompLogo.open()
                        }
                    }
                    Custom.HandMouseArea {
                        anchors.fill: deleteIcon
                        onClicked: {
                            backgroundDropArea.deletedImage = true
                            logoCell.tempLogoImg = ""
                        }
                    }
                }
            }
            DropArea {
                anchors.fill: backgroundDropArea
                enabled: true
                onEntered: {
                    canvas.enterArea()
                }
                onDropped: {
                    if (drop.hasUrls && drop.urls.length === 1) {
                        canvas.exitArea()
                        backgroundDropArea.deletedImage = false
                        app.company_module.upload_company_logo(drop.urls[0])
                    } else {
                         // TODO add popups
                         console.log("one file only")
                    }
                }
                onExited: {
                    canvas.exitArea()
                }
            }

            Item {
                id: btnUploadImgItem
                width: 176
                height: 40
                anchors {
                    left: backgroundDropArea.right
                    leftMargin: 24
                    bottom:  logoCell.bottom
                    bottomMargin: 3
                }
                Custom.Button {
                    id: btnUploadImg
                    width: 168
                    anchors.centerIn: parent
                    text: tr.a911_upload_logo
                    transparent: true
                    color: ui.colors.green1
                    onClicked: {
                        fileDialogCompLogo.open()
                    }
                }
            }

            Custom.TextFieldStatic {
                width: 300
                key: tr.a911_image_requirements
                value: tr.a911_drag_and_drop
                keyText.opacity: 1
                keyText.color: ui.colors.middle3
                valueText.color: ui.colors.middle3
                keyText.font.pixelSize: 12
                valueText.font.pixelSize: 12
                anchors {
                    top: backgroundDropArea.top
                    left: backgroundDropArea.right
                    leftMargin: 24
                    bottom: btnUploadImgItem.top
                    bottomMargin: 7
                    right: parent.right
                    rightMargin: 32
                }
            }

            Custom.FileDialogImages {
                id: fileDialogCompLogo
                onAccepted: {
                    if (fileDialogCompLogo.fileUrls.length === 1) {
                        backgroundDropArea.deletedImage = false
                        app.company_module.upload_company_logo(fileDialogCompLogo.fileUrl)
                    }
                    fileDialogCompLogo.close()
                }
            }

        }

        InfoCell {
            id: infoCell
            Layout.minimumHeight: 192
            Layout.maximumHeight: 192
            Layout.columnSpan: 2

            Column {
                spacing: 16
                width: parent.width - 32
                height: parent.height
                anchors {
                    left: parent.left
                }

                Rectangle {
                    width: 440
                    height: 40
                    radius: 10
                    color: installationToggle.checked ? ui.colors.dark1 : ui.colors.dark2
                    visible: false

                    Custom.FontText {
                        text: tr.a911_installer
                        width: parent.width - 64
                        color: ui.colors.white
                        font.pixelSize: 16
                        font.weight: Font.Light
                        wrapMode: Text.WordWrap
                        anchors {
                            left: parent.left
                            leftMargin: 16
                            verticalCenter: parent.verticalCenter
                        }
                    }

                    Custom.Toggle {
                        id: installationToggle

                        checked: false
                        anchors {
                            right: parent.right
                            rightMargin: 16
                            verticalCenter: parent.verticalCenter
                        }

                        mouseArea.onClicked: {
                            checked = !checked
                        }
                    }
                }

                Rectangle {
                    width: 440
                    height: 40
                    radius: 10
                    color: enabled && monitoringToggle.checked ? ui.colors.dark1 : ui.colors.dark2
                    enabled: false

                    Custom.FontText {
                        text: tr.a911_monitoring
                        width: parent.width - 64
                        color: ui.colors.white
                        font.pixelSize: 16
                        font.weight: Font.Light
                        wrapMode: Text.WordWrap
                        anchors {
                            left: parent.left
                            leftMargin: 16
                            verticalCenter: parent.verticalCenter
                        }
                    }

                    Custom.Toggle {
                        id: monitoringToggle

                        checked: true // false
                        anchors {
                            right: parent.right
                            rightMargin: 16
                            verticalCenter: parent.verticalCenter
                        }

                        mouseArea.onClicked: {
                            checked = !checked
                        }
                    }
                }

                Rectangle {
                    width: 440
                    height: 40
                    radius: 10
                    color: reactionToggle.checked ? ui.colors.dark1 : ui.colors.dark2
                    visible: false

                    Custom.FontText {
                        text: tr.a911_reaction
                        width: parent.width - 64
                        color: ui.colors.white
                        font.pixelSize: 16
                        font.weight: Font.Light
                        wrapMode: Text.WordWrap
                        anchors {
                            left: parent.left
                            leftMargin: 16
                            verticalCenter: parent.verticalCenter
                        }
                    }

                    Custom.Toggle {
                        id: reactionToggle

                        checked: false
                        anchors {
                            right: parent.right
                            rightMargin: 16
                            verticalCenter: parent.verticalCenter
                        }

                        mouseArea.onClicked: {
                            checked = !checked
                        }
                    }
                }
            }
        }


        InfoCell {
            id: addressHeaderCell
            Layout.columnSpan: 4

            Rectangle {
                height: 1
                color: ui.colors.white
                opacity: 0.1
                anchors {
                    top: parent.top
                    left: parent.left
                    right: parent.right
                }
            }

            Custom.FontText {
                font.pixelSize: 20
                text: tr.a911_legal_address
                color: ui.colors.white
                opacity: 0.5

                anchors {
                    bottom: parent.bottom
                    bottomMargin: 12
                    left: parent.left
                }
            }
        }


        InfoCell {
            id: addressCell
            Layout.columnSpan: 2
            Layout.rowSpan: 2

            Layout.minimumHeight: lawyerAddress.height + 24
            Layout.maximumHeight: lawyerAddress.height + 24

            Custom.TextAreaEdit {
                id: lawyerAddress
                width: parent.width
                key: tr.a911_street_house_office + ui.required
                value: ""
                distance: 12
                valueText.maximumLength: 200
                valueText.control.wrapMode: Text.WordWrap
                valueText.control.verticalAlignment: TextInput.AlignTop
                valueText.height: valueText.control.contentHeight + 24 < 136 ? 136 : valueText.control.contentHeight + 24
                valueText.control.height: valueText.control.contentHeight + 24 < 128 ? 128 : valueText.control.contentHeight + 24
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }

                valueText.control.onTextChanged: {
                    if (copy) {
                        postAddress.valueText.control.text = lawyerAddress.valueText.control.text
                    }
                }

                Connections {
                    target: app.company_module
                    onSaveCompanyValidationErrors: {
                        if (result["22.5"]) {
                            lawyerAddress.valueText.valid = false
                            lawyerAddress.valueText.error = result["22.5"].message
                        }
                    }
                }
            }
        }

        InfoCell {
            id: lawyerCountryCell
            Layout.minimumHeight: lawyerIndexField.height + 24
            Layout.maximumHeight: lawyerIndexField.height + 24

            /*Custom.TextFieldEdit {
                id: lawyerCountryField
                width: parent.width
                key: tr.country + ui.required
                valueText.control.maximumLength: 100
                value: ""
                distance: 12
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }

                Connections {
                    target: app.company_module
                    onSaveCompanyValidationErrors: {
                        if (result["22.1"]) {
                            lawyerCountryField.valueText.valid = false
                            lawyerCountryField.valueText.error = result["22.1"].message
                        }
                    }
                }
            }*/

            Custom.FontText {
                id: lawyerCountryKeyText
                text: tr.country + ui.required
                width: parent.width
                color: ui.colors.white
                opacity: 0.5
                font.pixelSize: 14
                font.weight: Font.Light
                wrapMode: Text.WordWrap
                anchors {
                    top: parent.top
                    topMargin: 13
                    left: parent.left
                }
            }

            Custom.CountriesCombobox {
                id: lawyerCountryValueText
                width: parent.width
                anchors {
                    top: lawyerCountryKeyText.bottom
                    topMargin: 8
                    left: parent.left
                }
                textLabel.control.onTextChanged: {
                    if (copy) {
                        postCountryValueText.code = lawyerCountryValueText.textLabel.control.text ? lawyerCountryValueText.code : ""
                    }
                }

                Connections {
                    target: scrollView.ScrollBar.vertical

                    onPositionChanged: {
                        lawyerCountryValueText.popup.close()
                    }
                }

                Connections {
                    target: app.company_module

                    onSaveCompanyValidationErrors: {
                        if (result["22.1"]) {
                            lawyerCountryValueText.textLabel.valid = false
                            lawyerCountryValueText.textLabel.error = tr.choose_country_from_the_list
                        }
                    }
                }
            }
        }

        InfoCell {
            id: lawyerIndexCell
            Layout.minimumHeight: lawyerIndexField.height + 24
            Layout.maximumHeight: lawyerIndexField.height + 24

            Custom.TextFieldEdit {
                id: lawyerIndexField
                width: parent.width
                key: tr.a911_zip_code + ui.required
                valueText.control.maximumLength: 20
                value: ""
                distance: 12
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }

                valueText.control.onTextChanged: {
                    if (copy) {
                        postIndexField.valueText.control.text = lawyerIndexField.valueText.control.text
                    }
                }

                Connections {
                    target: app.company_module
                    onSaveCompanyValidationErrors: {
                        if (result["22.4"]) {
                            lawyerIndexField.valueText.valid = false
                            lawyerIndexField.valueText.error = result["22.4"].message
                        }
                    }
                }
            }
        }

        InfoCell {
            id: lawyerCityCell
            Layout.minimumHeight: lawyerCityField.height + 24
            Layout.maximumHeight: lawyerCityField.height + 24

            Custom.TextFieldEdit {
                id: lawyerCityField
                width: parent.width
                key: tr.city + ui.required
                valueText.control.maximumLength: 100
                value: ""
                distance: 12
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }

                valueText.control.onTextChanged: {
                    if (copy) {
                        postCityField.valueText.control.text = lawyerCityField.valueText.control.text
                    }
                }

                Connections {
                    target: app.company_module
                    onSaveCompanyValidationErrors: {
                        if (result["22.3"]) {
                            lawyerCityField.valueText.valid = false
                            lawyerCityField.valueText.error = result["22.3"].message
                        }
                    }
                }
            }
        }

        InfoCell {
            id: lawyerAreaCell
            Layout.minimumHeight: lawyerAreaField.height + 24
            Layout.maximumHeight: lawyerAreaField.height + 24

            Custom.TextFieldEdit {
                id: lawyerAreaField
                width: parent.width
                key: tr.a911_region + ui.required
                valueText.control.maximumLength: 100
                value: ""
                distance: 12
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }

                valueText.control.onTextChanged: {
                    if (copy) {
                        postAreaField.valueText.control.text = lawyerAreaField.valueText.control.text
                    }
                }
            }

            Connections {
                target: app.company_module
                onSaveCompanyValidationErrors: {
                    if (result["22.2"]) {
                        lawyerAreaField.valueText.valid = false
                        lawyerAreaField.valueText.error = result["22.2"].message
                    }
                }
            }
        }

        InfoCell {
            Layout.columnSpan: 4

            Rectangle {
                height: parent.height
                anchors {
                    left: parent.left
                }

                Image {
                    id: logo
                    sourceSize.width: 32
                    sourceSize.height: 40
                    source: copy ? "qrc:/resources/images/facilities/a-badge-green.svg" : "qrc:/resources/images/facilities/a-badge-default.svg"
                    anchors {
                        verticalCenter: parent.verticalCenter
                    }

                    Custom.HandMouseArea {
                        onClicked: {
                            copy = !copy
                            postAddress.valueText.control.text = lawyerAddress.valueText.control.text
                            postCountryValueText.code = lawyerCountryValueText.textLabel.control.text ? lawyerCountryValueText.code : ""
                            postIndexField.valueText.control.text = lawyerIndexField.valueText.control.text
                            postCityField.valueText.control.text = lawyerCityField.valueText.control.text
                            postAreaField.valueText.control.text = lawyerAreaField.valueText.control.text
                        }
                    }
                }

                Custom.FontText {
                    text: tr.mail_legal_adress_matches
                    width: parent.width - 24
                    color: ui.colors.white
                    opacity: 0.5
                    font.pixelSize: 14
                    font.weight: Font.Light
                    wrapMode: Text.WordWrap
                    verticalAlignment: Text.AlignVCenter

                    anchors {
                        verticalCenter: parent.verticalCenter
                        left: logo.right
                        leftMargin: 8
                    }
                }
            }
        }

        InfoCell {
            id: postHeaderCell
            Layout.columnSpan: 4

            Rectangle {
                height: 1
                color: ui.colors.white
                opacity: 0.1
                anchors {
                    top: parent.top
                    left: parent.left
                    right: parent.right
                }
            }

            Custom.FontText {
                font.pixelSize: 20
                text: tr.a911_mail_address
                color: ui.colors.white
                opacity: 0.5

                anchors {
                    bottom: parent.bottom
                    bottomMargin: 12
                    left: parent.left
                }
            }
        }


        InfoCell {
            id: postCell
            Layout.columnSpan: 2
            Layout.rowSpan: 2

            Layout.minimumHeight: postAddress.height + 24
            Layout.maximumHeight: postAddress.height + 24

            Custom.TextAreaEdit {
                id: postAddress
                width: parent.width
                key: tr.a911_street_house_office + ui.required
                value: ""
                distance: 12
                valueText.maximumLength: 200
                valueText.control.wrapMode: Text.WordWrap
                valueText.control.verticalAlignment: TextInput.AlignTop
                valueText.height: valueText.control.contentHeight + 24 < 136 ? 136 : valueText.control.contentHeight + 24
                valueText.control.height: valueText.control.contentHeight + 24 < 128 ? 128 : valueText.control.contentHeight + 24
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }
                enabled: !copy

                Connections {
                    target: app.company_module
                    onSaveCompanyValidationErrors: {
                        if (result["23.5"]) {
                            postAddress.valueText.valid = false
                            postAddress.valueText.error = result["23.5"].message
                        }
                    }
                }
            }
        }

        InfoCell {
            id: postCountryCell
            Layout.minimumHeight: postIndexField.height + 24
            Layout.maximumHeight: postIndexField.height + 24

            /*Custom.TextFieldEdit {
                id: postCountryField
                width: parent.width
                key: tr.country + ui.required
                valueText.control.maximumLength: 200
                value: ""
                distance: 12
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }

                Connections {
                    target: app.company_module
                    onSaveCompanyValidationErrors: {
                        if (result["23.1"]) {
                            postCountryField.valueText.valid = false
                            postCountryField.valueText.error = result["23.1"].message
                        }
                    }
                }
            }*/

            Custom.FontText {
                id: postCountryKeyText
                text: tr.country + ui.required
                width: parent.width
                color: ui.colors.white
                opacity: 0.5
                font.pixelSize: 14
                font.weight: Font.Light
                wrapMode: Text.WordWrap
                anchors {
                    top: parent.top
                    topMargin: 13
                    left: parent.left
                }
            }

            Custom.CountriesCombobox {
                id: postCountryValueText
                width: parent.width
                anchors {
                    top: postCountryKeyText.bottom
                    topMargin: 8
                    left: parent.left
                }
                enabled: !copy

                Connections {
                    target: scrollView.ScrollBar.vertical

                    onPositionChanged: {
                        postCountryValueText.popup.close()
                    }
                }

                Connections {
                    target: app.company_module

                    onSaveCompanyValidationErrors: {
                        if (result["23.1"]) {
                            postCountryValueText.textLabel.valid = false
                            postCountryValueText.textLabel.error = tr.choose_country_from_the_list
                        }
                    }
                }
            }
        }

        InfoCell {
            id: postIndexCell
            Layout.minimumHeight: postIndexField.height + 24
            Layout.maximumHeight: postIndexField.height + 24

            Custom.TextFieldEdit {
                id: postIndexField
                width: parent.width
                key: tr.a911_zip_code + ui.required
                valueText.control.maximumLength: 20
                value: ""
                distance: 12
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }
                enabled: !copy

                Connections {
                    target: app.company_module
                    onSaveCompanyValidationErrors: {
                        if (result["23.4"]) {
                            postIndexField.valueText.valid = false
                            postIndexField.valueText.error = result["23.4"].message
                        }
                    }
                }
            }
        }

        InfoCell {
            id: postCityCell
            Layout.minimumHeight: postCityField.height + 24
            Layout.maximumHeight: postCityField.height + 24

            Custom.TextFieldEdit {
                id: postCityField
                width: parent.width
                key: tr.city + ui.required
                valueText.control.maximumLength: 100
                value: ""
                distance: 12
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }
                enabled: !copy

                Connections {
                    target: app.company_module
                    onSaveCompanyValidationErrors: {
                        if (result["23.3"]) {
                            postCityField.valueText.valid = false
                            postCityField.valueText.error = result["23.3"].message
                        }
                    }
                }
            }
        }

        InfoCell {
            id: postAreaCell
            Layout.minimumHeight: postAreaField.height + 24
            Layout.maximumHeight: postAreaField.height + 24

            Custom.TextFieldEdit {
                id: postAreaField
                width: parent.width
                key: tr.a911_region + ui.required
                valueText.control.maximumLength: 100
                value: ""
                distance: 12
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }
                enabled: !copy

                Connections {
                    target: app.company_module
                    onSaveCompanyValidationErrors: {
                        if (result["23.2"]) {
                            postAreaField.valueText.valid = false
                            postAreaField.valueText.error = result["23.2"].message
                        }
                    }
                }
            }
        }

        InfoCell {
            id: regCell
            Layout.columnSpan: 4
            Layout.minimumHeight: 112
            Layout.maximumHeight: 112

            Rectangle {
                height: 1
                color: ui.colors.white
                opacity: 0.1
                anchors {
                    top: parent.top
                    left: parent.left
                    right: parent.right
                }
            }

            Item {
                width: parent.width
                height: 40
                anchors {
                    top: parent.top
                    topMargin: 12
                }

                Custom.HandMouseArea {
                    visible: toggleText.hoveredLink != ""
                }

                Custom.Toggle {
                    id: agreementToggle

                    anchors {
                        verticalCenter: parent.verticalCenter
                    }

                    mouseArea.onClicked: {
                        agreementToggle.checked = !agreementToggle.checked
                    }
                }

                Custom.FontText {
                    id: toggleText
                    width: parent.width - 96
                    height: contentHeight
                    text: tr.i_have_read_and_agree + ": " + "<a style='text-decoration:none' href='agreement'>" + util.colorize(tr.a911_terms_of_use, ui.colors.green1) + "</a>" + ", " + "<a style='text-decoration:none' href='privacy'>" + util.colorize(tr.a911_privacy_policy, ui.colors.green1) + "</a>" + ", " + "<a style='text-decoration:none' href='license'>" + util.colorize(util.insert(tr.ajax_software_license_agreement, ["", "", ""]), ui.colors.green1) + "</a>"
                    color: ui.colors.light3
                    lineHeight: 1.1
                    font.pixelSize: 12
                    font.weight: Font.Light
                    elide: Text.ElideRight
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignLeft | Text.AlignVCenter
                    anchors {
                        verticalCenter: parent.verticalCenter
                        left: agreementToggle.right
                        leftMargin: 24
                    }

                    onLinkActivated: {
                        var locale = tr.get_locale()
                        locale = locale == "uk" ? "ua" : locale
                        locale = locale == "pt_PT" ? "pt" : locale

                        if (link == "agreement") {
                            link = "https://ajax.systems/" + locale + "/end-user-agreement/"
                            Qt.openUrlExternally(link)
                            return
                        }

                        if (link == "privacy") {
                            link = "https://ajax.systems/" + locale + "/privacy-policy/"
                            Qt.openUrlExternally(link)
                            return
                        }

                        if (link == "license") {
                            link = "https://ajax.systems/" + locale + "/ajax-pro-agreement/"
                            Qt.openUrlExternally(link)
                            return
                        }
                    }
                }
            }

            Item {
                width: 384
                height: parent.height - 60
                anchors {
                    bottom: parent.bottom
                    horizontalCenter: parent.horizontalCenter
                }

                Custom.Button {
                    width: 384
                    text: tr.a911_send_request
                    transparent: false
                    color: ui.colors.green1
                    anchors.centerIn: parent
                    enabledCustom: {
                        return agreementToggle.checked

                        fullNameField.valueText.control.text.length > 0 && declarationField.valueText.control.text.length > 0
                        && shortNameField.valueText.control.text.length > 0 && phoneField.valueText.control.text.length > 0 &&
                        emailField.valueText.control.text.length > 0 && lawyerAddress.valueText.control.text.length > 0 &&
                        lawyerCityField.valueText.control.text.length > 0 &&
                        lawyerCountryValueText.textLabel.control.text.length > 0 && lawyerAreaField.valueText.control.text.length > 0 &&
                        lawyerIndexField.valueText.control.text.length > 0 && postAddress.valueText.control.text.length > 0 &&
                        postCityField.valueText.control.text.length > 0 && postCountryValueText.textLabel.control.text.length > 0 &&
                        postAreaField.valueText.control.text.length > 0 && postIndexField.valueText.control.text.length > 0
                    }

                    onClicked: {
                        application.debug("pro -> company -> create company")

                        var settings = {}
                        settings["full_name"] = fullNameField.valueText.control.text.trim()
                        settings["short_name"] = shortNameField.valueText.control.text.trim()
                        settings["head_of_company"] = ceoField.valueText.control.text.trim()
                        settings["registration_number"] = declarationField.valueText.control.text.trim()

                        settings["phone_numbers"] = [{"number": phoneField.valueText.control.text.trim()}]
                        settings["email_addresses"] = [{"email": emailField.valueText.control.text.trim()}]

                        settings["provided_services"] = {"installation": installationToggle.checked, "monitoring": monitoringToggle.checked, "reaction": reactionToggle.checked}

                        settings["legal_address"] = {"address_line1": lawyerAddress.valueText.control.text.trim(), "city": lawyerCityField.valueText.control.text.trim(), "state": lawyerAreaField.valueText.control.text.trim(), "zip_code": lawyerIndexField.valueText.control.text.trim()}
                        var legalCode = util.get_country_code(application.countries.countries, lawyerCountryValueText.textLabel.control.text.trim())
                        settings["legal_address"]["country"] = legalCode

                        settings["postal_address"] = {"address_line1": postAddress.valueText.control.text.trim(), "city": postCityField.valueText.control.text.trim(), "state": postAreaField.valueText.control.text.trim(), "zip_code": postIndexField.valueText.control.text.trim()}
                        var postalCode = util.get_country_code(application.countries.countries, postCountryValueText.textLabel.control.text.trim())
                        settings["postal_address"]["country"] = postalCode

                        if (logoCell.tempLogoImg) {
                            settings["company_logo"] = {"image_id": "", "images": []}
                            settings["company_logo"]['image_id'] = logoCell.imageId
                            settings["company_logo"]["images"] = [{'resolution': '128x128', 'url': logoCell.tempLogoImg}]
                        }
                        if (backgroundDropArea.deletedImage) {
                            settings["company_logo"] = {"image_id": "", "images": []}
                        }
                        app.company_module.create_company(settings)
                    }
                }

                Connections {
                    target: app.company_module
                    onSaveCompanyValidationErrors: {
                        if (result["3"] || result["6"] || result["7"] || result["4"] || result["21[0].1"] || result["20[0].1"]) {
                            scrollBarAnim.to = 0
                            scrollBarAnim.start()
                        }
                    }
                }
            }
        }

        InfoCell { Layout.columnSpan: 4 }
    }
}
