# Websocket通信 jsonフォーマット

## 1. プレイヤー名要求
### 1.1. プレイヤー名要求
```
{
    "type": "object",
    "state": {
        "type": "string",
        "const": "connect"
    },
    "messageType": {
        "type": "string,
        "const": "requestPlayerName"
    },
    "body": {
        "type": "object"
        "message":{
            "type":"string",
            "const":"Please tell your player name."
        }
    }
}
```

### 1.2. プレイヤー名応答
```
{
    "type": "object",
    "messageType": {
        "type": "string,
        "const": "requestPlayerName"
    },
    "body": {
        "type": "object",
        "playerName": {
            "type": "string"
        }
    }
}

```

## 2. プレイヤー番号通知
```
{
    "type": "object",
    "state": {
        "type": "string",
        "const": "matching",
    },
    "messageType": {
        "type": "string",
        "const": "tellPlayerNumber"
    },
    "body": {
        "type": "object",
        "playerNumber": {
            "type": "number"
        }
    }
}
```

## 3. 初期数値設定
### 3.1. 初期数値設定要求
```
{
    "type": "object",
    "state": {
        "type": "string",
        "const": "start_game"
    },
    "messageType": {
        "type": "string",
        "const": "requestSecretNumber"
    },
    "body": {
        "type": "object"
        "message":{
            "type":"string",
            "const":"Please tell your secret number."
        }
    }
}
```

## 3.2. 初期数値設定応答
```
{
    "type": "object",
    "messageType": {
        "type": "string",
        "const": "requestSecretNumber"
    },
    "body": {
        "type": "object",
        "number": {
            "type": "string"
        }
    }
}
```

## 4. チャレンジ
### 4.1. チャレンジ要求
```
{
    "type": "object",
    "state": {
        "type": "string",
        "const": "in-game"
    },
    "messageType": {
        "type": "stirng",
        "const": "requestChallengeNumber"
    },
    "body": {
        "type": "object",
        "message":{
            "type": "string",
            "const": "Please call challenge number."
        }
    }
}
```

### 4.2. チャレンジ応答
```
{
    "type": "object",
    "messageType": {
        "type": "stirng",
        "const": "requestChallengeNumber"
    },
    "body": {
        "type": "object",
        "action": {
            "type": "string",
            "const": "call"
        },
        "number": {
            "type": "string"
        }
    }
}
```

## 5. アイテム使用
### 5.1. アイテム使用要求
```
{
    "type": "object",
    "state": {
        "type": "string",
        "const": "in-game"
    },
    "messageType": {
        "type": "stirng",
        "const": "requestItemAction"
    },
    "body": {
        "type": "object",
        "message":{
            "type":"string",
            "const":"Please tell the item you use."
        }
    }
}
```

### 5.2. アイテム使用応答 使用なし
```
{
    "type": "object",
    "messageType": {
        "type": "stirng",
        "const": "requestItemAction-pass"
    },
    "body": {
        "type": "object",
        "action": {
            "type": "string",
            "const": "pass"
        }
    }
}
```

### 5.3. アイテム使用応答 ターゲット
```
{
    "type": "object",
    "messageType": {
        "type": "stirng",
        "const": "requestItemAction-target"
    },
    "body": {
        "type": "object",
        "action": {
            "type": "string",
            "const": "target"
        },
        "number": {
            "type": "string",
        }
    }
}
```

### 5.4. アクション応答 ハイ&ロー
```
{
    "type": "object",
    "messageType": {
        "type": "stirng",
        "const": "requestItemAction-high-low"
    },
    "body": {
        "type": "object",
        "action": {
            "type": "string",
            "const": "high-low"
        }
    }
}
```

### 5.5. アクション応答 シャッフル
```
{
    "type": "object",
    "messageType": {
        "type": "stirng",
        "const": "requestItemAction-shuffle"
    },
    "body": {
        "type": "object",
        "action": {
            "type": "string",
            "const": "shuffle"
        },
        "number": {
            "type": "string"
        }
    }
}
```

### 5.6. アクション応答 チェンジ
```
{
    "type": "object",
    "messageType": {
        "type": "stirng",
        "const": "requestItemAction-change"
    },
    "body": {
        "type": "object",
        "action": {
            "const": "change"
        },
        "number": {
            "type": "string"
        }
    }
}
```

## 6. 結果通知
### 6.1. チャレンジ結果通知
```
{
    "type": "object",
    "state": {
        "type": "string",
        "const": "in-game"
    },
    "messageType": {
        "type": "string",
        "const": "challengeResult"
    },
    "body": {
        "type": "object",
        "action": {
            "type": "string",
            "const": "challenge"
        },
        "playerNumber": {
            "type": "number
        },
        "result": {
            "type": "object",
            "number": {
                "type": "string"
            },
            "hit": {
                "type": "number"
            },
            "blow": {
                "type": "number"
            }
        }
    }
}
```

### 6.2. アイテム使用結果通知 使用なし
```
{
    "type": "object",
    "state": {
        "type": "string",
        "const": "in-game"
    },
    "messageType": {
        "type": "stirng",
        "const": "itemActionResult-pass"
    },
    "body": {
        "type": "object",
        "action": {
            "type": "string",
            "const": "pass"
        },
        "playerNumber": {
            "type": "number
        },
        "result": {
            "type": "object"
        }
    }
}
```

### 6.3. アイテム使用結果通知 ターゲット
```
{
    "type": "object",
    "state": {
        "type": "string",
        "const": "in-game"
    },
    "messageType": {
        "type": "string",
        "const": "itemActionResult-target"
    },
    "body": {
        "type": "object",
        "action": {
            "type": "string",
            "const": "target"
        },
        "playerNumber": {
            "type": "number
        },
        "result": {
            "type": "object",
            "number": {
                "type": "string"
            },
            "position": {
                "type": "number"
            }
        }
    }
}
```

### 6.4. アイテム使用結果通知 ハイ&ロー
```
{
    "type": "object",
    "state": {
        "type": "string",
        "const": "in-game"
    },
    "messageType": {
        "type": "string",
        "const": "itemActionResult-high-low"
    },
    "body": {
        "type": "object",
        "action": {
            "type": "high-low"
        },
        "playerNumber": {
            "type": "number
        },
        "result": {
            "type": "object",
            "high": {
                "type": "number"
            },
            "low": {
                "type": "number"
            }
        }
    }
}
```

### 6.5. アイテム使用結果通知 シャッフル
```
{
    "type": "object",
    "state": {
        "type": "string",
        "const": "in-game"
    },
    "messageType": {
        "type": "string",
        "const": "itemActionResult-shuffle"
    },
    "body": {
        "type": "object",
        "action": {
            "type": "string",
            "const": "shuffle"
        },
        "playerNumber": {
            "type": "number
        },
        "result": {
            "type": "object"
        }
    }
}
```

### 6.6. アイテム使用結果通知 チェンジ
```
{
    "type": "object",
    "state": {
        "type": "string",
        "const": "in-game"
    },
    "messageType": {
        "type": "string",
        "const": "itemActionResult-change"
    },
    "body": {
        "type": "object",
        "action": {
            "type": "string",
            "const": "change"
        },
        "playerNumber": {
            "type": "number
        },
        "result": {
            "type": "object",
            "position": {
                "type": number
            },
            "high-low": {
                "type": "string",
                "enum": [
                    "high",
                    "low"
                ]
            }
        }
    }
}
```

## 7. 相手プレイヤーアクション結果通知
```
{
    "type": "object",
    "state": {
        "type": "string",
        "const": "in-game"
    },
    "messageType": {
        "type": "string",
        "const": "opponentActionResult"
    },
    "body": {
        "type": "object",
        "actionResults": {
            "type": "array",
            "items": {
                "oneOf": [
                    {
                        "type": "object",
                        "action": {
                            "type": "string",
                            "const": "challenge"
                        },
                        "playerNumber": {
                            "type": "number 
                        },
                        "result": {
                            "type": "object",
                            "number": {
                                "type": "string"
                            },
                            "hit": {
                                "type": "number"
                            },
                            "blow": {
                                "type": "number"
                            }
                        }
                    },
                    {
                        "type": "object",
                        "action": {
                            "type": "string",
                            "const": "target"
                        },
                        "playerNumber": {
                            "type": "number
                        },
                        "result": {
                            "type": "object",
                            "number": {
                                "type": "string"
                            },
                            "position": {
                                "type": "number"
                            }
                        }
                    },
                    {
                        "type": "object",
                        "action": {
                            "type": "high-low"
                        },
                        "playerNumber": {
                            "type": "number
                        },
                        "result": {
                            "type": "object",
                            "high": {
                                "type": "number"
                            },
                            "low": {
                                "type": "number"
                            }
                        }
                    },
                    {
                        "type": "object",
                        "action": {
                            "type": "string",
                            "const": "shuffle"
                        },
                        "playerNumber": {
                            "type": "number
                        },
                        "result": {
                            "type": "object"
                        }
                    },
                    {
                        "action": {
                            "type": "string",
                            "const": "change"
                        },
                        "playerNumber": {
                            "type": "number
                        },
                        "result": {
                            "type": "object",
                            "digit": {
                                "type": number
                            },
                            "high-low": {
                                "type": "string",
                                "enum": [
                                    "high",
                                    "low"
                                ]
                            }
                        }
                    }
                ]
            }
        }
    }
}
```

## 8. ラウンド結果通知
```
{
    "type": "object",
    "state": {
        "type": "string",
        "const": "in-game"
    },
    "messageType": {
        "type": "string",
        "const": "roundResult"
    },
    "body": {
        "type": "object",
        "winnerPlayerNumber": {
            "type": "number"
        }
    }
}
```

## 9. ゲーム結果通知
```
{
    "type": "object",
    "state": {
        "type": "string",
        "const": "finish-game"
    },
    "messageType": {
        "type": "string",
        "const": "gameResult"
    },
    "body": {
        "type": "object",
        "winnerPlayerNumber": {
            "type": "number"
        }
    }
}
```
