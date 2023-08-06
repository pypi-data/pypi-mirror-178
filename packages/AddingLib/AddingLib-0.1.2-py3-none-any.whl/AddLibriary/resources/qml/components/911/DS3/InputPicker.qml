import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3



DS3.MasterInputPicker {
    onInputTextChanged: () => {
        let bestMatch = find(input.atomInput.text, Qt.MatchStartsWith)
        if (bestMatch == -1) {
            input.errorText = notIncludedErrorText
        }
        scrollToIndex(bestMatch)
    }
    onPickerActivated: () => {
        if (customHighlightedIndex != -1) {
            currentIndex = customHighlightedIndex
            input.atomInput.text = model[currentIndex]
        }
        else {
            if (currentIndex == -1) {
                input.atomInput.text = ""
            }
            else {
                input.atomInput.text = model[currentIndex]
            }
        }
    }
    onInputActiveFocusChanged: () => {
        input.errorText = ""
        if (input.atomInput.activeFocus) popup.open()
        if (!input.atomInput.activeFocus) {
            if (currentIndex == -1) {
                input.atomInput.text = ""
            }
            else {
                input.atomInput.text = model[currentIndex]
            }
        }
    }
}