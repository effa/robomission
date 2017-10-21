export function getLevelStatus(state) {
  const level = state.student.level;
  const activeCredits = state.student.activeCredits;
  // current level specify number of credits the student needs to level up
  const maxCredits = state.levels[level].credits;
  return { level, activeCredits, maxCredits };
}


export function isNewStudent(state) {
  return state.student.credits === 0;
}


export function getStudentUrl(state) {
  // TODO:  move studentUrl to student substate
  return state.user.studentUrl;
}


export function getPracticeOverviewUrl(state) {
  return state.student.practiceOverviewUrl;
}


export function getSolveTaskUrl(state) {
  return state.student.solveTaskUrl;
}


export function getReportProgramExecutionUrl(state) {
  return state.student.reportProgramExecutionUrl;
}


export function getReportProgramEditUrl(state) {
  return state.student.reportProgramEditUrl;
}
