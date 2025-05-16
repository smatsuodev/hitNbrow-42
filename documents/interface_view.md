## プレイヤー名/プレイヤー番号通知
```
{
    "type": "object",
    "state": {
        "type": "string",
        "const": "matching",
    },
    "messageType": {
        "type": "string,
        "const": "sendPlayerName"
    },
    "body": {
        "type": "object",
        "players": {
            "type": "array",
            "items": {
                "type": "object",
                "playerNumber": {
                    "type": "number"
                }
                "playerName": {
                    "type": "string"
                }
            }
        }
    }
}
```

## 初期数値設定通知
```
{
    "type": "object",
    "state": {
        "type": "string",
        "const": "start-game"
    },
    "messageType": {
        "type": "string",
        "const": "sendSecretNumber"
    },
    "body": {
        "type": "object",
        "secrets": {
            "type": "array",
            "items": {
                "type": "object",
                "playerNumber": {
                    "type": "number"
                },
                "number": {
                    "type": "string"
                }
            }
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
        "number": {
            "type": "string"
        },
        "result": {
            "type": "object",
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
            "type": "number"
        },
        "result": {
            "type": "object",
            "number": {
                "type": "string"
            }
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
        },
        "points": {
            "type": "array",
            "items": {
                "type": "object",
                "playerNumber": {
                    "type": "number"
                },
                "point": {
                    "type": "number"
                }
            }
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
        },
        "points": {
            "type": "array",
            "items": {
                "type": "object",
                "playerNumber": {
                    "type": "number"
                },
                "point": {
                    "type": "number"
                }
            }
        }
    }
}
```
