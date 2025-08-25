# 🔔 Signals Overview

Bu hujjatda har bir app uchun yozilgan signal funksiyalarining maqsadi va avtomatik yaratiladigan modellar ko‘rsatiladi.

---

## 🧑‍⚕️ doctor app

| Yaratuvchi model | Avtomatik to‘ldiriladigan model(lar)                         | Izoh                                                         |
|------------------|---------------------------------------------------------------|--------------------------------------------------------------|
| Doctor           | History, WorkingHour, SecuritySetting                         | Doktor yaratilganda tarix yozuvi, default ish vaqti, xavfsizlik sozlamalari yaratiladi. |

---

## 👤 user app

| Yaratuvchi model | Avtomatik to‘ldiriladigan model | Izoh                                          |
|------------------|----------------------------------|-----------------------------------------------|
| User             | Profile                          | Foydalanuvchi yaratilganda `Profile` avtomatik yaratiladi. |

---

## 🏥 clinic app

| Yaratuvchi model | Avtomatik to‘ldiriladigan model | Izoh                                      |
|------------------|----------------------------------|-------------------------------------------|
| ❌               | ❌                                | Hozircha hech qanday avtomatik to‘ldirish yo‘q. |

---

## 📅 appointment app

| Yaratuvchi model | Avtomatik to‘ldiriladigan model | Izoh                                      |
|------------------|----------------------------------|-------------------------------------------|
| ❌               | ❌                                | Hozircha hech qanday avtomatik to‘ldirish yo‘q. |

---

## ⚙️ system app

| Yaratuvchi model | Avtomatik to‘ldiriladigan model | Izoh                                      |
|------------------|----------------------------------|-------------------------------------------|
| ❌               | ❌                                | Hozircha hech qanday avtomatik to‘ldirish yo‘q. |

---

## 🔄 Eslatma

- Har bir signal `apps.py` ichida `import signals` orqali chaqirilgan bo‘lishi **shart**.
- Agar biron-bir signal ishlamayotgan bo‘lsa, quyidagilarni tekshiring:
  - Signal funksiyasi `@receiver` bilan yozilganmi?
  - Signal fayli `apps.py > ready()` ichida import qilinganmi?
  - `created=True` shartiga tushayaptimi?

---
