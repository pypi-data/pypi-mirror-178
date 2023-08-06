import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


Item {
    id: countryPhones

    property var countryPhonesModel: util.country_codes_from_data()
    property string phoneText: countryPhonesModel[countryPhoneCombo.currentIndex].number + countryPhoneField.control.text

    property alias valueText: countryPhoneField
    property alias key: keyText.text
    property alias countryPhoneCombo: countryPhoneCombo

    /* ---------------------------------------------------- */
    /* desktop tests */
    property var accessibleKeyName: ""
    property var accessibleKeyDescription: ""

    property var accessibleValueName: ""
    property var accessibleValueDescription: ""
    /* ---------------------------------------------------- */

    width: 800
    height: keyText.contentHeight + countryPhone.height + 7

    Desktop.NormalText {
        id: keyText

        text: tr.phone
        color: ui.colors.white
        opacity: 0.5
    }

    Item {
        id: countryPhone

        width: parent.width
        height: countryPhoneField.height

        anchors.bottom: parent.bottom

        Custom.ComboBoxNew {
            id: countryPhoneCombo

            width: 120
            currentIndex: -1
            defaultText: "+..."

            model: countryPhonesModel

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
                    horizontalAlignment: Text.AlignLeft

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
                        horizontalAlignment: Text.AlignLeft

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

            width: countryPhone.width - countryPhoneCombo.width - 40

            control {
                rightPadding: 8
                maximumLength: 30
                validator: RegExpValidator { regExp : /[0-9]{1,30}/ }
            }

            anchors {
                top: parent.top
                topMargin: 5
                left: countryPhoneCombo.right
                leftMargin: 8
            }

            control.onTextChanged: {
                if (!countryPhones.phoneNumbers || !countryPhones.phoneNumbers[countryPhone.itemIndex]) return

                countryPhones.phoneNumbers[countryPhone.itemIndex]["phoneField"] = control.text.trim()
                countryPhones.phoneNumbersChanged()
            }
        }
    }
}
