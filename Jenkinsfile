node {
   stage 'Clean'
   sh "git reset --hard HEAD"
   sh "git clean -f -d -x"

   // Mark the code checkout 'stage'....
   stage 'Checkout'

   // Get some code from a GitHub repository
   git url: 'https://github.com/parkerjb22/avarts.git'

   stage 'Unit tests'
   sh "nose2 --plugin nose2.plugins.junitxml --junit-xml tests -C"

   step([$class: 'JUnitResultArchiver', testResults: 'nose2-junit.xml'])
}