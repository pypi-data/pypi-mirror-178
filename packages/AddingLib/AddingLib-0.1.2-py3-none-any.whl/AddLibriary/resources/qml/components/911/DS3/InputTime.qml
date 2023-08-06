import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    id: inputTime

//  Time in seconds
    property real time: 0
//  Minimal time that could be entered
    property real minimalTime: 5

    readonly property real realMinutes: parseInt(minutes.input.atomInput.text)
    readonly property real realSeconds: parseInt(seconds.input.atomInput.text)

    function timeEdit() {
        minutes.input.atomInput.text = Math.max(
            realMinutes,
            Math.floor(minimalTime / 60)
        ).toString().padStart(2, "0")

        seconds.input.atomInput.text = (Math.max(
            realMinutes * 60 + realSeconds,
            minimalTime
        ) - realMinutes * 60).toString().padStart(2, "0")

        time = realMinutes * 60 + realSeconds
    }

    width: parent.width
    height: Math.max(minutes.height, seconds.height)

    DS3.InputPicker {
        id: minutes

        anchors {
            left: parent.left
            right: parent.horizontalCenter
            rightMargin: 1
        }

        onInputTextChanged: () => {
            const bestMatch = find(input.atomInput.text, Qt.MatchStartsWith)
            if (bestMatch != -1) {
                scrollToIndex(bestMatch)
            }
        }

        input {
            regex: ui.regexes.scenario_minutes
            atomInput {
                label: tr.minutes
                text: Math.floor(time / 60).toString().padStart(2, "0")
                onEditingFinished: timeEdit()
                onActiveFocusChanged: {
                    if (!input.atomInput.activeFocus && !input.atomInput.text) input.atomInput.text = "00"
                    timeEdit()
                }
            }
        }
        model: util.generate_minutes_for_scenarios()
    }

    DS3.MasterInputPicker {
        id: seconds

        anchors {
            left: parent.horizontalCenter
            right: parent.right
        }

        onInputTextChanged: () => {
            const bestMatch = find(input.atomInput.text, Qt.MatchStartsWith)
            if (bestMatch != -1) {
                scrollToIndex(bestMatch)
            }
            else {
                customHighlightedIndex = -1
            }
        }

        onActivated: () => {
            currentIndex = customHighlightedIndex
            if (currentIndex != -1) {
                input.atomInput.text = model[currentIndex]
            }
        }
        onInputActiveFocusChanged: () => {
            if (input.atomInput.activeFocus) seconds.popup.open()
            if (!input.atomInput.activeFocus) {
                if (customHighlightedIndex != -1 && !!input.atomInput.text) {
                    input.atomInput.text = model[currentIndex]
                }
            }
        }

        input {
            regex: ui.regexes.scenario_seconds
            atomInput {
                label: tr.seconds
                text: (parseInt(time) % 60).toString().padStart(2, "0")
                onEditingFinished: timeEdit()
                onActiveFocusChanged: {
                    if (!input.atomInput.activeFocus && !input.atomInput.text) input.atomInput.text = "00"
                    timeEdit()
                }
            }
        }
        model: util.generate_seconds_for_scenarios()
    }
}
