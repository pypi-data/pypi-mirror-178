import os

from filter_vcf.filter_vcf import filter_vcf


def test_filter_vcf():

    vcf_file = f"{os.path.dirname(os.path.abspath(__file__))}/sample.nrm.vcf.gz"

    result = filter_vcf(vcf_file, "PASS:sb")

    os.remove(vcf_file.replace("nrm.vcf.gz", "nrm.filtered.vcf.gz"))

    assert result is not None
