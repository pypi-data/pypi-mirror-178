import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


Item {
    id: countryPhones

    width: useDescription ? parent.width : 484
    height: keyText.contentHeight + listView.contentHeight + distance

    signal errorResult(variant result)

    property var key: ""
    property var model: []

    property var maxCount: 0
    property var distance: 0
    property var fieldDistance: 0

    property var useFooter: true
    property var useDescription: false
    property var atLeastOneField: false
    property var plusItemVisible: true
    property var fieldMinLength: 0
    property var errorProperty: ""

    property var defaultCountry: ""
    property var defaultItem: {
        return {"phoneCode": countryPhones.getCountryCodeItem(defaultCountry)["info"], "phoneField": "", "description": ""}
    }

    property alias keyText: keyText
    property alias listView: listView

    property var phoneNumbers: []
    property var itemsCollection: {
        var items = []
        phoneNumbers.forEach(function(item) {
            items.push({"number": item.phoneCode.number + item.phoneField, "country_code": item.phoneCode.code, "description": item.description})
        })
        return items
    }

    property var active: {
        for (var i = 0; i < itemsCollection.length; i++) {
            var item = listView.itemAtIndex(i)
            if (item && item.active) return true
        }
        return false
    }

    function addItem() {
        countryPhones.focus = true
        countryPhones.listView.model = countryPhones.listView.model.concat([countryPhones.defaultItem])
    }

    function getCountryCodeItem(selectedCountry) {
        if (!selectedCountry) return {"index": -1, "info": {"code": "", "number": "", "description": ""}}
        for (var i = 0; i < countryPhones.countriesModel.length; i++) {
            if (countryPhones.countriesModel[i].code.toLowerCase() == selectedCountry.toLowerCase()) {
                return {"index": i, "info": countryPhones.countriesModel[i]}
            }
        }
        return {"index": -1, "info": {"code": "", "number": "", "description": ""}}
    }

    //  <--------------  CountryCode & CountryPhone Model  --------------->
    property var countriesModel: []

    Connections {
        target: application

        onCountriesChanged: {
            if (!application.countries || countryPhones.countriesModel.length) return
            countryPhones.countriesModel = util.country_codes_for_regions(application.countries.countries)
        }
    }

    Component.onCompleted: {
        if (!application.countries || countryPhones.countriesModel.length) return
        countryPhones.countriesModel = util.country_codes_for_regions(application.countries.countries)
    }
    //  >-----------------------------------------------------------------<

    Desktop.NormalText {
        id: keyText

        text: countryPhones.key
        color: ui.colors.secondary
    }

    ListView {
        id: listView

        width: parent.width
        interactive: false
        spacing: fieldDistance

        anchors {
            top: keyText.bottom
            topMargin: model.length > 0 ? fieldDistance : 4
            left: parent.left
            bottom: parent.bottom
        }

        onModelChanged: {
            var items = []
            listView.model.forEach(function(item) {
                items.push(item)
            })
            countryPhones.phoneNumbers = items
        }

        delegate: Item {
            id: countryPhone

            width: parent.width - 40
            height: countryPhoneField.height

            property var itemIndex: index
            property var active: countryPhoneCombo.comboPopup.opened || countryPhoneField.control.activeFocus || countryPhoneDescription.control.activeFocus

            Custom.ComboBoxNew {
                id: countryPhoneCombo

                width: useDescription ? 120 : countryPhone.width * 0.4
                currentIndex: -1
                defaultText: "+..."

                model: countryPhones.countriesModel

                /*
                backgroundRectangle {
                    topRightCorner: false
                    bottomRightCorner: false
                }
                */

                onModelChanged: {
                    countryPhoneCombo.currentIndex = countryPhones.getCountryCodeItem(modelData.phoneCode.code)["index"]
                }

                onActivated: {
                    var phoneItem = {"phoneCode": countryPhoneCombo.model[countryPhoneCombo.currentIndex], "phoneField": countryPhoneField.control.text.trim(), "description": countryPhoneDescription.control.text.trim()}
                    listView.model = listView.model.slice(0, countryPhone.itemIndex).concat(phoneItem, listView.model.slice(countryPhone.itemIndex + 1, listView.model.length))
                }

                contentItem: Item {
                    width: countryPhoneCombo.width
                    height: 40

                    Image {
                        id: contentImage

                        width: 24
                        height: 24
                        source: {
                            if (countryPhoneCombo.currentIndex == -1) return "qrc:/resources/images/desktop/countries/earth.png"
                            return "qrc:/resources/images/desktop/countries/" + countryPhoneCombo.model[countryPhoneCombo.currentIndex].code.toLowerCase() + ".png"
                        }

                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: parent.left
                            leftMargin: 8
                        }
                    }

                    Custom.FontText {
                        id: countryPhoneComboText

                        width: parent.width - 40
                        color: ui.colors.white
                        text: {
                            if (countryPhoneCombo.currentIndex == -1) return countryPhoneCombo.defaultText
                            var objItem = countryPhoneCombo.model[countryPhoneCombo.currentIndex]
                            return objItem && objItem.number ? objItem.number : countryPhoneCombo.defaultText
                        }

                        opacity: countryPhoneCombo.currentIndex == -1 ? 0.5 : 1
                        wrapMode: Text.NoWrap
                        textFormat: Text.PlainText
                        font: countryPhoneCombo.font
                        verticalAlignment: Text.AlignVCenter

                        anchors {
                            left: contentImage.right
                            leftMargin: 12
                            verticalCenter: parent.verticalCenter
                        }
                    }
                }

                delegate: ItemDelegate {
                    id: delegateItem

                    width: countryPhoneCombo.width
                    height: 40

                    background: Rectangle {
                        color: hovered ? ui.colors.dark3 : ui.colors.dark1
                        width: parent.width
                        height: delegateItem.height
                    }

                    contentItem: Item {
                        Image {
                            id: contentImageDelegate

                            width: 24
                            height: 24
                            source: "qrc:/resources/images/desktop/countries/" + modelData.code.toLowerCase() + ".png"

                            anchors {
                                verticalCenter: parent.verticalCenter
                                left: parent.left
                            }
                        }

                        Custom.FontText {
                            width: parent.width - 48
                            color: ui.colors.white
                            text: modelData.number

                            wrapMode: Text.NoWrap
                            elide: Text.ElideRight
                            textFormat: Text.PlainText
                            font: countryPhoneCombo.font
                            verticalAlignment: Text.AlignVCenter

                            anchors {
                                left: contentImageDelegate.right
                                leftMargin: 12
                                verticalCenter: parent.verticalCenter
                            }
                        }
                    }
                }
            }

            Custom.TextField {
                id: countryPhoneField

                width: useDescription ? 200 : countryPhone.width * 0.6 - 8

                control {
                    text: modelData.phoneField
                    rightPadding: !useDescription && deleteImage.visible ? 48 : 8
                    maximumLength: 30
                    validator: RegExpValidator { regExp : /[0-9]{1,30}/ }
                }

                anchors {
                    top: parent.top
                    topMargin: 5
                    left: countryPhoneCombo.right
                    leftMargin: useDescription ? 4 : 8
                }

                Image {
                    id: deleteImage

                    width: 24
                    height: 24

                    sourceSize {
                        width: 40
                        height: 40
                    }

                    source: "qrc:/resources/images/icons/control-a-minus-button.svg"
                    visible: {
                        if (useDescription) return false
                        return countryPhones.atLeastOneField ? listView.model.length > 1 : listView.model.length > 0
                    }

                    anchors {
                        verticalCenter: countryPhoneField.background.verticalCenter
                        right: parent.right
                        rightMargin: 8
                    }

                    Custom.HandMouseArea {
                        onClicked: {
                            var listViewVar = listView
                            var indexVar = index
                            focus = true
                            listViewVar.model = listViewVar.model.slice(0, indexVar).concat(listViewVar.model.slice(indexVar + 1, listViewVar.model.length))
                        }
                    }
                }

                control.onTextChanged: {
                    if (!countryPhones.phoneNumbers || !countryPhones.phoneNumbers[countryPhone.itemIndex]) return

                    countryPhones.phoneNumbers[countryPhone.itemIndex]["phoneField"] = control.text.trim()
                    countryPhones.phoneNumbersChanged()
                }

                control.onEditingFinished: {
                    var phoneItem = {"phoneCode": countryPhoneCombo.model[countryPhoneCombo.currentIndex], "phoneField": countryPhoneField.control.text.trim(), "description": countryPhoneDescription.control.text.trim()}
                    listView.model = listView.model.slice(0, countryPhone.itemIndex).concat(phoneItem, listView.model.slice(countryPhone.itemIndex + 1, listView.model.length))
                }
            }

            Custom.TextField {
                id: countryPhoneDescription

                visible: useDescription

                placeHolderText: tr.phone_desc
                width: countryPhone.width - countryPhoneCombo.width - countryPhoneField.width - 4 - 16

                control {
                    text: modelData.description ? modelData.description : ""
                    rightPadding: deleteImageAlt.visible ? 48 : 8
                    maximumLength: 255
                }

                anchors {
                    top: parent.top
                    topMargin: 5
                    left: countryPhoneField.right
                    leftMargin: 16
                }

                Image {
                    id: deleteImageAlt

                    width: 24
                    height: 24

                    sourceSize {
                        width: 40
                        height: 40
                    }

                    source: "qrc:/resources/images/icons/control-a-minus-button.svg"
                    visible: countryPhones.atLeastOneField ? listView.model.length > 1 : listView.model.length > 0

                    anchors {
                        verticalCenter: countryPhoneDescription.background.verticalCenter
                        right: parent.right
                        rightMargin: 8
                    }

                    Custom.HandMouseArea {
                        onClicked: {
                            var listViewVar = listView
                            var indexVar = index
                            focus = true
                            listViewVar.model = listViewVar.model.slice(0, indexVar).concat(listViewVar.model.slice(indexVar + 1, listViewVar.model.length))
                        }
                    }
                }

                control.onTextChanged: {
                    if (!countryPhones.phoneNumbers || !countryPhones.phoneNumbers[countryPhone.itemIndex]) return

                    countryPhones.phoneNumbers[countryPhone.itemIndex]["description"] = control.text.trim()
                    countryPhones.phoneNumbersChanged()
                }

                control.onEditingFinished: {
                    var phoneItem = {"phoneCode": countryPhoneCombo.model[countryPhoneCombo.currentIndex], "phoneField": countryPhoneField.control.text.trim(), "description": countryPhoneDescription.control.text.trim()}
                    listView.model = listView.model.slice(0, countryPhone.itemIndex).concat(phoneItem, listView.model.slice(countryPhone.itemIndex + 1, listView.model.length))
                }
            }

            Connections {
                target: countryPhones

                onErrorResult: {
                    var errorValue = `${countryPhones.errorProperty}[${index}].1`

                    if (result[errorValue]) {
                        countryPhoneField.valid = false
                        // countryPhoneField.error = result[errorValue].message
                    }
                }
            }
        }

        footer: Item {
            width: parent.width - 40
            height: {
                if (!visible) return 1
                return listView.model.length > 0 ? 40 + countryPhones.fieldDistance : 43
            }

            visible: {
                if (listView.model.length == 0) return true

                if (!countryPhones.useFooter) return false
                return countryPhones.maxCount ? (countryPhones.maxCount > listView.model.length) && countryPhones.plusItemVisible : countryPhones.plusItemVisible
            }

            Item {
                width: parent.width
                height: parent.height

                visible: listView.model.length == 0

                anchors.bottom: parent.bottom

                Image {
                    width: 24
                    height: 24

                    sourceSize {
                        width: 40
                        height: 40
                    }

                    anchors.verticalCenter: parent.verticalCenter

                    source: "qrc:/resources/images/icons/control-a-plus-button.svg"

                    Custom.HandMouseArea {
                        onClicked: {
                            addItem()
                        }
                    }
                }
            }

            Rectangle {
                width: parent.width
                height: 40
                radius: height / 2
                color: ui.colors.dark1
                anchors.bottom: parent.bottom

                visible: listView.model.length != 0

                Image {
                    width: 24
                    height: 24

                    sourceSize {
                        width: 40
                        height: 40
                    }

                    source: "qrc:/resources/images/icons/control-a-plus-button.svg"

                    anchors.centerIn: parent

                    Custom.HandMouseArea {
                        onClicked: {
                            addItem()
                        }
                    }
                }
            }
        }

        Component.onCompleted: {
            if (countryPhones.model.length == 0) {
                if (countryPhones.atLeastOneField) {
                    countryPhones.model = countryPhones.model.concat([countryPhones.defaultItem])
                } else {
                    countryPhones.model = []
                }
            }
            listView.model = countryPhones.model
        }
    }

    Item {
        width: 40
        height: 40

        visible: {
            if (countryPhones.useFooter) return false
            if (listView.model.length == 0) return false
            return countryPhones.maxCount ? (countryPhones.maxCount > listView.model.length) && countryPhones.plusItemVisible : countryPhones.plusItemVisible
        }

        anchors {
            right: parent.right
            bottom: parent.bottom
            bottomMargin: useDescription ? 0 : 2
        }

        Image {
            width: 24
            height: 24

            sourceSize {
                width: 40
                height: 40
            }

            source: "qrc:/resources/images/icons/control-a-plus-button.svg"

            anchors.centerIn: parent

            Custom.HandMouseArea {
                onClicked: {
                    addItem()
                }
            }
        }
    }
}
