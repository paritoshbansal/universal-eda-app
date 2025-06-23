# Universal EDA Report

**Target**: PassengerId

**Detected task**: Regression

**Dropped columns**: Name, Ticket

## EDA Takeaways
- When Survived = 0, average PassengerId = 447.02
- When Survived = 1, average PassengerId = 444.37
- When Pclass = 1, average PassengerId = 461.60
- When Pclass = 2, average PassengerId = 445.96
- When Pclass = 3, average PassengerId = 439.15
- When Sex = female, average PassengerId = 431.03
- When Sex = male, average PassengerId = 454.15
- When SibSp = 0, average PassengerId = 455.37
- When SibSp = 1, average PassengerId = 439.73
- When SibSp = 2, average PassengerId = 412.43
- When SibSp = 3, average PassengerId = 321.56
- When SibSp = 4, average PassengerId = 381.61
- When SibSp = 5, average PassengerId = 336.80
- When SibSp = 8, average PassengerId = 481.71
- When Parch = 0, average PassengerId = 445.26
- When Parch = 1, average PassengerId = 465.11
- When Parch = 2, average PassengerId = 416.66
- When Parch = 3, average PassengerId = 579.20
- When Parch = 4, average PassengerId = 384.00
- When Parch = 5, average PassengerId = 435.20
- When Parch = 6, average PassengerId = 679.00
- When Embarked = C, average PassengerId = 445.36
- When Embarked = Q, average PassengerId = 417.90
- When Embarked = S, average PassengerId = 449.53
- When Embarked = nan, average PassengerId = 446.00

## 📈 Trend Insights
✅ Passengerid increases with Survived
✅ Passengerid increases with Pclass
✅ Passengerid increases with Sex
✅ Passengerid increases with SibSp
✅ Passengerid increases with Parch
✅ Passengerid increases with Embarked

### ✅ Best-Case Scenario:
- Cabin is one of: A10, A14, A16, A19, A20, A23, A24, A26, A31, A32, A34, A36, A5, A6, A7, B101, B102, B18, B19, B20, B22, B28, B3, B30, B35, B37, B38, B39, B4, B41, B42, B49, B5, B50, B51 B53 B55, B57 B59 B63 B66, B58 B60, B69, B71, B73, B77, B78, B79, B80, B82 B84, B86, B94, B96 B98, C101; Embarked is one of: C, Q, S; Age <= 39.5 (younger)
- Outcome: **621.38**

### ❌ Worst-Case Scenario:
- Cabin is one of: A10, A14, A16, A19, A20, A23, A24, A26, A31, A32, A34, A36, A5, A6, A7, B101, B102, B18, B19, B20, B22, B28, B3, B30, B35, B37, B38, B39, B4, B41, B42, B49, B5, B50, B51 B53 B55, B57 B59 B63 B66, B58 B60, B69, B71, B73, B77, B78, B79, B80, B82 B84, B86, B94, B96 B98, C101; Embarked is one of: nan
- Outcome: **62.00**