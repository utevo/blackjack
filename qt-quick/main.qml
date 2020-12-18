import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import Model 1.0 // https://stackoverflow.com/questions/57742024/custom-object-referencing-in-qml-python


Window {
    id: root
    width: 1000
    height: 600
    visible:  true

    Model {
        id: mainModel
    }

    Rectangle {
        color: 'green'
        anchors.fill: parent

        GridLayout {
            columns: 4
            anchors.fill: parent

            anchors.margins: 30


            Text {}

            Label {
                text: "Cards"
            }

            Label {
                text: "Values"
            }

            Label {
                text: "Points"
            }

            Label {
                text: "You"
            }

            Row {
                Layout.alignment: Qt.AlignCenter
                Layout.preferredWidth: 350
                spacing: 5

                Repeater {
                    model: mainModel.player_cards

                    Card {
                        size: 30
                        rank: modelData[0]
                        suit: modelData[1]
                    }
                }
            }

            Row {
                Layout.alignment: Qt.AlignCenter
                spacing: 5

                Repeater {
                    model: mainModel.player_values
                    ValueLabel {
                        text: modelData
                    }
                }
            }

            ValueLabel {
                text: mainModel.player_points
            }

            Label {
                text: "Casino"
            }

            Row {
                Layout.alignment: Qt.AlignCenter
                Layout.preferredWidth: 350
                spacing: 5

                Repeater {
                    model: mainModel.casino_cards

                    Card {
                        size: 30
                        rank: modelData[0]
                        suit: modelData[1]
                    }
                }
            }

            Row {
                Layout.alignment: Qt.AlignCenter
                spacing: 5
                Repeater {
                    model: mainModel.casino_values
                    ValueLabel {
                        text: modelData
                    }
                }
            }

            ValueLabel {
                text: mainModel.casino_points
                color: 'red'
            }
        }

        Row {
            id: buttons

            anchors.bottom: parent.bottom
            anchors.margins: 5
            anchors.horizontalCenter: parent.horizontalCenter

            spacing: 5

            Layout.rowSpan: 4

            Button {
                id: hitButton
                text: 'Hit'
                Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                onClicked: mainModel.hit()

                enabled: mainModel.player_turn
                font.pointSize: 20
            }

            Button {
                id: standButton
                text: 'Stand'
                Layout.alignment: Qt.AlignLeft | Qt.AlignBottom
                onClicked: mainModel.stand()

                enabled: mainModel.player_turn
                font.pointSize: 20
            }
        }

        Rectangle {
            anchors.centerIn: parent
            visible: mainModel.message == '' ? false : true

            Text {
                text: mainModel.message
                font.pixelSize: 20
                font.bold: true
            }
        }
    }

    component Card: Rectangle {
        property int size: 50
        property string rank
        property string suit
        width: size * 2.5
        height: size * 3.5
        radius: 5
        color: 'white'
        border.color: 'black'

        RotationAnimation on rotation {
            from: 0; to: 360;
            duration: 1000
        }

        Column {
            anchors.centerIn: parent
            Text {
                font.pixelSize: parent.parent.size * 0.7
                text: rank
                anchors.horizontalCenter: parent.horizontalCenter
            }
            Image {
                height: parent.parent.size
                width: parent.parent.size
                source: `./images/${suit}.svg`
                fillMode: Image.PreserveAspectFit
            }
        }
    }

    component Label: Rectangle {
        property string text
        Layout.alignment: Qt.AlignCenter
        width: 150
        height: 60
        color: 'yellow'
        border.color: 'black'

        Text {
            anchors.centerIn: parent
            text: parent.text
            font.pixelSize: 20
            font.bold: true
        }
    }

    component ValueLabel: Rectangle {
        property string text
        Layout.alignment: Qt.AlignCenter
        width: 35
        height: 35
        color: 'red'
        border.color: 'black'

        Text {
            anchors.centerIn: parent
            text: parent.text
            font.pixelSize: 15
            font.bold: true
        }
    }
}
