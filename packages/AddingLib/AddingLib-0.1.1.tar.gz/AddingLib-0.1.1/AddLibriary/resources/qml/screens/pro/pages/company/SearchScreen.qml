import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


Item {
    id: companySearchScreen

    property var companyNameDefault: ""
    property var countryCodeDefault: ""

    Rectangle {
        width: parent.width / 5
        height: searchScreenExplainTip.height + 72
        radius: 10
        color: ui.colors.black

        anchors {
            top: parent.top
            topMargin: 16
            right: parent.right
            rightMargin: 16
        }

        Image {
            source: "qrc:/resources/images/pro/company/create-company-warning.svg"
            sourceSize.width: 24
            sourceSize.height: 24

            anchors {
                top: parent.top
                topMargin: 16
                left: parent.left
                leftMargin: 16
            }
        }

        Item {
            height: 24

            anchors {
                top: parent.top
                topMargin: 16
                left: parent.left
                leftMargin: 48
                right: parent.right
                rightMargin: 16
            }

            Custom.FontText {
                id: searchScreenOwnerText

                text: tr.create_company_tip_title
                color: ui.colors.yellow1

                font.pixelSize: 16
                font.bold: true
                wrapMode: Text.Wrap
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignVCenter

                anchors.fill: parent
            }
        }

        Item {
            id: searchScreenExplainTip

            width: parent.width - 32
            height: searchScreenExplainTipText.contentHeight

            anchors {
                top: parent.top
                topMargin: 56
                bottom: parent.bottom
                bottomMargin: 16
                horizontalCenter: parent.horizontalCenter
            }

            Custom.FontText {
                id: searchScreenExplainTipText

                text: tr.create_company_tip
                color: ui.colors.light3

                font.pixelSize: 14
                wrapMode: Text.Wrap
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignTop

                anchors.fill: parent
            }
        }
    }

    Item {
        id: searchScreenHeader

        width: parent.width * 0.5
        height: searchScreenHeaderText.contentHeight

        anchors {
            top: parent.top
            topMargin: 48
            horizontalCenter: parent.horizontalCenter
        }

        Custom.FontText {
            id: searchScreenHeaderText

            text: tr.company_creation_title
            color: ui.colors.light3

            font.pixelSize: 32
            font.bold: true
            wrapMode: Text.Wrap
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignVCenter

            anchors.fill: parent
        }
    }

    Item {
        id: searchScreenExplain

        width: parent.width * 0.5
        height: searchScreenExplainText.contentHeight

        anchors {
            top: searchScreenHeader.bottom
            topMargin: 16
            horizontalCenter: parent.horizontalCenter
        }

        Custom.FontText {
            id: searchScreenExplainText

            text: tr.company_creation_what_enter
            color: ui.colors.light3

            font.pixelSize: 16
            wrapMode: Text.Wrap
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignTop

            anchors.fill: parent
        }
    }


    Item {
        id: searchScreenName

        width: parent.width * 0.5
        height: 80

        anchors {
            top: searchScreenExplain.bottom
            topMargin: 48
            horizontalCenter: parent.horizontalCenter
        }

        Custom.TextFieldEdit {
            id: searchScreenNameField

            width: parent.width
            distance: 12
            key: tr.field_company_name
            value: companySearchScreen.companyNameDefault

            keyText.opacity: 1
            keyText.color: ui.colors.secondary
            valueText.control.maximumLength: 100
        }

        ToolTip {
            id: nameToolTip

            width: 236
            height: nameContentText.contentHeight + 24

            x: -(width + 16)
            y: (parent.height - height) / 2 + 8

            visible: searchScreenNameField.valueText.control.activeFocus

            contentItem: Custom.FontText {
                id: nameContentText

                color: ui.colors.light3
                text: tr.hover_company_name

                font.pixelSize: 12
                wrapMode: Text.Wrap
                textFormat: Text.PlainText
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter

                anchors.centerIn: parent
            }

            background: Rectangle {
                radius: 8
                color: ui.colors.dark4
                anchors.fill: parent
            }
        }
    }

    Item {
        id: searchScreenCountry

        width: parent.width * 0.5
        height: 72

        anchors {
            top: searchScreenName.bottom
            topMargin: 32
            horizontalCenter: parent.horizontalCenter
        }

        Item {
            width: 400
            height: parent.height

            Custom.FontText {
                id: searchScreenCountryText

                text: tr.field_company_country_work
                color: ui.colors.secondary

                font.pixelSize: 14
                wrapMode: Text.Wrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
            }

            Custom.CountriesCombobox {
                id: searchScreenCountryCombo

                width: parent.width

                code: companySearchScreen.countryCodeDefault
                maxPopupHeight: 300
                badgeImageMargin: 4
                includeWorldwide: false
                textLabel.placeHolderText: ""

                anchors {
                    top: searchScreenCountryText.bottom
                    topMargin: 8
                }
            }

            ToolTip {
                id: countryToolTip

                width: 236
                height: countryContentText.contentHeight + 24

                x: -(width + 16)
                y: (parent.height - height) / 2 + 8

                visible: searchScreenCountryCombo.countriesPopup.opened

                contentItem: Custom.FontText {
                    id: countryContentText

                    color: ui.colors.light3
                    text: tr.hover_company_country_work

                    font.pixelSize: 12
                    wrapMode: Text.Wrap
                    textFormat: Text.PlainText
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter

                    anchors.centerIn: parent
                }

                background: Rectangle {
                    radius: 8
                    color: ui.colors.dark4
                    anchors.fill: parent
                }
            }
        }
    }


    Item {
        id: searchScreenContinue

        width: parent.width * 0.5
        height: 48

        anchors {
            bottom: parent.bottom
            bottomMargin: 32
            horizontalCenter: parent.horizontalCenter
        }

        Item {
            width: searchScreenContinueButton.textButton.contentWidth + 64
            height: parent.height

            anchors.left: parent.left

            Custom.Button {
                id: searchScreenContinueButton

                width: parent.width
                text: tr.continue_
                textButton.textFormat: Text.PlainText
                enabledCustom: companyCode && companyName.length > 1

                anchors.centerIn: parent

                property var companyName: searchScreenNameField.valueText.control.text.trim()
                property var companyCode: util.get_country_code(searchScreenCountryCombo.originModel, searchScreenCountryCombo.textLabel.control.text.trim())

                onClicked: {
                    var settings = {
                        "search_phrase": companyName,
                        "country_code": companyCode,
                    }

                    app.company_module.search_companies(settings)
                }
            }
        }
    }

    Desktop.BackArea {
        backArea.onClicked: {
            companyLoader.source = companyStack.startScreen
        }
    }

    Connections {
        target: app.company_module

        onSearchCompaniesFound: {
            companyLoader.setSource(companyStack.foundScreen, {"companies": companies, "companyName": searchScreenContinueButton.companyName, "countryCode": searchScreenContinueButton.companyCode})
        }

        onSearchCompaniesNotFound: {
            var companyInfo = {
                "userID": appUser.user_id,
                "name": searchScreenContinueButton.companyName,
                "code": searchScreenContinueButton.companyCode,
            }
            companyInfo = settings.storage_get("companies_creation", companyInfo)

            companyLoader.setSource(companyStack.createScreen, {"companyName": searchScreenContinueButton.companyName, "countryCode": searchScreenContinueButton.companyCode, "companyInfo": companyInfo})
        }
    }
}
