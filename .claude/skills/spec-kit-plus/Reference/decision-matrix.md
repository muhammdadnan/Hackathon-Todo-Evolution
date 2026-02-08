# Decision Matrix

## Confidence-Based Decisions

| Confidence | Range | Action |
|------------|-------|--------|
| HIGH | >85% | Auto-proceed |
| MEDIUM | 50-85% | Proceed + Log |
| LOW | <50% | Ask User |

## Auto-Decision Categories

| Category | Auto-Decision | User Required |
|----------|--------------|---------------|
| Skill Selection | ✅ | - |
| Phase Transition | ✅ | - |
| Standard Patterns | ✅ | - |
| Architecture | - | ✅ ADR |
| Breaking Changes | - | ✅ Consent |
| Scope Changes | - | ✅ Approval |

## Logging Format

```
[timestamp] [type] [category] [confidence] [action] [outcome]
```
