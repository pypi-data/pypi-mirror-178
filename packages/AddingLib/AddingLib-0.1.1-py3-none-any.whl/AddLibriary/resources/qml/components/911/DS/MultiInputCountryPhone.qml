import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/911/DS" as DS


// Multi input field for phone numbers, that consist of country code(in combobox) and phone body(in field)
DS.MultiInputField {
    id: countryPhones

//  Default country code for each new phone number
    property var defaultCountry: ""

//  Method to check if all phone number are valid
    function checkValid() {
        var valid = true
        for (var index in listData) {
            var item = countryPhones.get(index)

            if (item.countryPhoneCombo.currentIndex == -1) {
                item.countryPhoneCombo.error = true
                valid = false
            }
            else item.countryPhoneCombo.error = false

            if (!item.countryPhoneField.checkValid()) valid = false
        }
        return valid
    }

//  Method to add new phone field
    function addItem() {
        listData.push({"country_code": countryPhones.getCountryCodeItem(defaultCountry).info.code, "number": "", "description": ""})
        listDataChanged()
    }

//  Method to get full country code info based on the code
    function getCountryCodeItem(selectedCountry) {
        if (!selectedCountry) return {"index": -1, "info": {"country_code": "", "number": ""}}
        for (var i = 0; i < countryPhones.countriesModel.length; i++) {
            if (countryPhones.countriesModel[i].code.toLowerCase() == selectedCountry.toLowerCase()) {
                return {"index": i, "info": countryPhones.countriesModel[i]}
            }
        }
        return {"index": -1, "info": {"country_code": "", "number": ""}}
    }

//  Method to collect data accordingly to the proto
    function collectData() {
        var numbers = []
        for (var item of listData) {
            numbers.push({
                "country_code": item.country_code,
                "number": getCountryCodeItem(item.country_code).info.number + item.number,
                "description": item.description ? item.description.trim() : ""
            })
        }
        return numbers
    }

    //  Do not touch this
    //  <--------------  CountryCode & CountryPhone Model  --------------->
    property var countriesModel: []

    function guessCountryCodes() {
        var prefferedCountryNumber = countryPhones.getCountryCodeItem(defaultCountry).info.number || undefined

        for (var i in listData) {
            var item = listData[i]
            if (!item.country_code) {
                if (item.number.startsWith(prefferedCountryNumber)) {
                    listData[i].country_code = defaultCountry
                    listData[i].number = item.number.slice(prefferedCountryNumber.length, item.number.length)
                } else if (item.number.startsWith("+")) {
                    var guessed_country_item = countriesModel.filter(
                        (country) => item.number.startsWith(country.number)
                    )[0]
                    listData[i].country_code = guessed_country_item.code
                    listData[i].number = item.number.slice(guessed_country_item.number.length, item.number.length)
                }
            } else {
                listData[i].number = item.number.slice(
                    countryPhones.getCountryCodeItem(item.country_code).info.number.length,
                    item.number.length
                )
            }
        }
        listDataChanged()
    }

    canBeEmpty: true

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
        guessCountryCodes()
    }
    //  >-----------------------------------------------------------------<

    footer: Item {
        width: parent.width
        height: visible ? footerButton.height : 0

        visible: listData.length == 0

        DS.ButtonRound {
            id: footerButton

            style: ui.controls.plus

            onClicked: addItem()
        }
    }

    delegateItem: Item {
        id: countryPhone

        width: parent.width
        height: countryPhoneField.height

        property alias countryPhoneCombo: countryPhoneCombo
        property alias countryPhoneField: countryPhoneField
        property var listDataIndex: index
        property var forcedError: ""

        onForcedErrorChanged: if (!!forcedError) countryPhoneField.forcedError = forcedError

        DS.Combobox {
            id: countryPhoneCombo

            width: 130
            currentIndex: -1
            defaultText: "+..."

            model: countryPhones.countriesModel

            onModelChanged: countryPhoneCombo.currentIndex = countryPhones.getCountryCodeItem(modelData.country_code)["index"]

            onActivated: {
                listData[listDataIndex].country_code = countryPhoneCombo.model[countryPhoneCombo.currentIndex].code
                checkReadyToSave()
            }

            contentItem: Item {
                width: countryPhoneCombo.width
                height: 40

                Image {
                    id: contentImage

                    width: 24
                    height: 24

                    anchors {
                        verticalCenter: parent.verticalCenter
                        left: parent.left
                        leftMargin: 12
                    }

                    source: {
                        if (countryPhoneCombo.currentIndex == -1) return "qrc:/resources/images/desktop/countries/earth.png"
                        return "qrc:/resources/images/desktop/countries/" + countryPhoneCombo.model[countryPhoneCombo.currentIndex].code.toLowerCase() + ".png"
                    }
                }

                DS.Text {
                    id: countryPhoneComboText

                    anchors {
                        left: contentImage.right
                        leftMargin: 8
                        verticalCenter: parent.verticalCenter
                    }

                    size: 16
                    action: false
                    text: {
                        if (countryPhoneCombo.currentIndex == -1) return countryPhoneCombo.defaultText
                        var objItem = countryPhoneCombo.model[countryPhoneCombo.currentIndex]
                        return objItem && objItem.number ? objItem.number : countryPhoneCombo.defaultText
                    }
                    opacity: countryPhoneCombo.currentIndex == -1 ? 0.5 : 1
                }
            }

            delegateItem: Item {
                Image {
                    id: contentImageDelegate

                    width: 24
                    height: 24

                    anchors {
                        verticalCenter: parent.verticalCenter
                        left: parent.left
                    }

                    source: "qrc:/resources/images/desktop/countries/" + delegateModelData.code.toLowerCase() + ".png"
                }

                DS.Text {
                    anchors {
                        left: contentImageDelegate.right
                        leftMargin: 12
                        verticalCenter: parent.verticalCenter
                    }

                    text: delegateModelData.number
                    size: 16

                    Binding on color {
                        when: delegateIndex == countryPhoneCombo.currentIndex
                        value: ui.colors.interactive
                    }
                }
            }
        }

        DS.InputField {
            id: countryPhoneField

            width: 160

            anchors {
                left: countryPhoneCombo.right
                leftMargin: 1
            }

            validator: RegExpValidator { regExp: /[0-9]+/ }
            value: modelData.number
            required: true
            minimumLength: 3
            maximumLength: 30
            lengthError: tr.from_3_to_200_characters_911

            onEdited: {
                listData[index].number = value
                checkReadyToSave()
            }

            onForcedErrorChanged: countryPhone.forcedError = countryPhoneField.forcedError
        }

        Item {
            id: fakePanel

            width: 17
            height: countryPhoneCombo.height

            anchors {
                left: countryPhoneCombo.right
                leftMargin: -8
            }

            clip: true

            Rectangle {
                width: 9
                height: parent.height

                anchors {
                    left: parent.left
                    leftMargin: -1
                }

                color: ui.backgrounds.highest
                border {
                    color: countryPhoneCombo.error ? ui.colors.attention : ui.colors.interactive
                    width: countryPhoneCombo.error || countryPhoneCombo.popup.visible ? 1 : 0
                }
            }

            Rectangle {
                width: 9
                height: parent.height

                anchors {
                    right: parent.right
                    rightMargin: -1
                }

                color: ui.backgrounds.highest
                border {
                    color: countryPhoneField.valid ? ui.colors.interactive : ui.colors.attention
                    width: (countryPhoneField.valueItem.activeFocus || !countryPhoneField.valid) ? 1 : 0
                }
            }
        }

        DS.InputField {
            id: description

            width: 300

            anchors {
                left: countryPhoneField.right
                leftMargin: 8
            }

            value: modelData.description ? modelData.description : ""
            hasPlusButton: index + 1 == list.count && maxCount > list.count && countryPhoneField.value.length > 0
            hasMinusButton: countryPhones.required ? list.count != 1 : true
            placeholder: tr.phone_desc
            maximumLength: 255

            onPlusClicked: addItem()
            onMinusClicked: listData = [...listData.splice(0, index), ...listData.splice(1, listData.length)]
            onEdited: {
                listData[index].description = value
                checkReadyToSave()
            }
        }
    }
}
