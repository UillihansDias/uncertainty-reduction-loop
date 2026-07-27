/**
 * Uncertainty Reduction Loop Hook for OpenClaw.
 * Injects a compact reminder during agent bootstrap.
 */

const REMINDER_NAME = 'UNCERTAINTY_REDUCTION_LOOP_REMINDER.md';
const REMINDER_PATH = REMINDER_NAME;

const REMINDER_CONTENT = `
## Uncertainty Reduction Loop Reminder

Use the uncertainty-reduction loop when the correct answer, cause, or implementation is not known in advance.

Rules:
- Propose one testable hypothesis or approach.
- Implement the smallest reversible experiment.
- Run it and capture actual output.
- Validate with exactly one status: VALIDATED, PARTIALLY_VALIDATED, INVALIDATED, or INCONCLUSIVE.
- Learn by separating observation from interpretation.
- Select the next action by expected uncertainty reduction.
- Do not call something fixed, solved, confirmed, or working before execution and validation.
`.trim();

function isObject(value) {
  return !!value && typeof value === 'object';
}

function isInjectedReminderFile(value) {
  if (!isObject(value) || value.path !== REMINDER_PATH) return false;
  return value.virtual === true || value.content === REMINDER_CONTENT;
}

const handler = async (event) => {
  if (!event || typeof event !== 'object') return;
  if (event.type !== 'agent' || event.action !== 'bootstrap') return;
  if (!event.context || typeof event.context !== 'object') return;

  const sessionKey = event.sessionKey || '';
  if (sessionKey.includes(':subagent:')) return;

  if (Array.isArray(event.context.bootstrapFiles)) {
    const occupiedByOtherFile = event.context.bootstrapFiles.some(
      (file) => isObject(file) && file.path === REMINDER_PATH && !isInjectedReminderFile(file),
    );
    if (occupiedByOtherFile) return;

    const cleanedBootstrapFiles = event.context.bootstrapFiles.filter(
      (file, index, files) =>
        !isInjectedReminderFile(file) ||
        files.findIndex((candidate) => isInjectedReminderFile(candidate)) === index,
    );

    const reminderFile = {
      name: REMINDER_NAME,
      path: REMINDER_PATH,
      content: REMINDER_CONTENT,
      missing: false,
      virtual: true,
    };

    const existingIndex = cleanedBootstrapFiles.findIndex((file) => isInjectedReminderFile(file));
    if (existingIndex === -1) cleanedBootstrapFiles.push(reminderFile);
    else cleanedBootstrapFiles[existingIndex] = reminderFile;

    event.context.bootstrapFiles = cleanedBootstrapFiles;
  }
};

module.exports = handler;
module.exports.default = handler;
