# flake8_iw

### IW01: Use of patch

Lint check to prevent the use of `patch` directly.
Recommendation: Use `PatchingTestCase` / `PatchingTransactionTestCase` instead

```python
from unittest.mock import patch
from unittest.mock import patch as patch_alias

class SignUpUpdatedTests(TestCase):
    def setUp(self):
        self.patcher = patch("apps.auth.signals.task_send_email.delay")

    def test_created(self, mock_task):
        self.mock_call = patch_alias("apps.auth.signals.task_send_email.delay")
        ...
```
