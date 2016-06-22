node {
   stage 'Checkout'
   git url: 'https://github.com/parkerjb22/avarts.git'

   stage 'Unit tests'
   sh "nose2 --plugin nose2.plugins.junitxml --junit-xml tests -C"

   step([$class: 'JUnitResultArchiver', testResults: 'nose2-junit.xml'])
}