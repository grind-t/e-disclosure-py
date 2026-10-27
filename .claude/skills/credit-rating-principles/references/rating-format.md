# Формат оценки

Оценка — одна запись из массива `ratings` в `exports/companies.json`:

```json
{
  "period": "2026, 6 месяцев",
  "value": 16,
  "outlook": "STA",
  "promptVersion": 8,
  "model": "claude-opus-5-5",
  "analyzedAt": "2026-10-26"
}
```

| Поле | Значение |
|---|---|
| `period` | Период отчета: `2025` для годового, `2026, 3 месяца`, `2026, 6 месяцев`, `2026, 9 месяцев` для промежуточных |
| `value` | Рейтинг: индекс в шкале ниже |
| `outlook` | Прогноз: `STA` — стабильный, `POS` — позитивный, `NEG` — негативный, `DEV` — развивающийся |
| `promptVersion` | Поле `version` из frontmatter навыка |
| `model` | Точный ID модели, которая выставила оценку |
| `analyzedAt` | Дата оценки в формате `YYYY-MM-DD` |

## Шкала

| value | Рейтинг | value | Рейтинг | value | Рейтинг |
|---|---|---|---|---|---|
| 0 | ruD | 8 | ruB- | 16 | ruBBB+ |
| 1 | ruC | 9 | ruB | 17 | ruA- |
| 2 | ruCC- | 10 | ruB+ | 18 | ruA |
| 3 | ruCC | 11 | ruBB- | 19 | ruA+ |
| 4 | ruCC+ | 12 | ruBB | 20 | ruAA- |
| 5 | ruCCC- | 13 | ruBB+ | 21 | ruAA |
| 6 | ruCCC | 14 | ruBBB- | 22 | ruAA+ |
| 7 | ruCCC+ | 15 | ruBBB | 23 | ruAAA |

## Соответствие глобальной шкале

По S&P Global Ratings' National And Regional Scale Mapping Tables (14.08.2017), Russia Mapping Table — последняя таблица S&P для России. Если глобальному уровню соответствует несколько ступеней, выбери ступень по Methodology For National And Regional Scale Credit Ratings (2018).

| Глобальная шкала | value | Рейтинг |
|---|---|---|
| bbb- и выше | 23 | ruAAA |
| bb+ | 22 | ruAA+ |
| bb | 21 | ruAA |
| bb- | 20 | ruAA- |
| b+ | 19, 18 | ruA+, ruA |
| b | 18, 17, 16 | ruA, ruA-, ruBBB+ |
| b- | 15, 14 | ruBBB, ruBBB- |
| ccc+ | 13, 12, 11 | ruBB+, ruBB, ruBB- |
| ccc | 10, 9, 8 | ruB+, ruB, ruB- |
| ccc- | 7, 6, 5 | ruCCC+, ruCCC, ruCCC- |
| cc | 3 | ruCC |
| c | 1 | ruC |
| sd, d | 0 | ruD |
